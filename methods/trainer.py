import torch
from torch import distributed
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel
from utils.loss import HardNegativeMining, FocalLoss, KnowledgeDistillationLoss, EntropyLoss
from .segmentation_module import make_model
from modules.classifier import IncrementalClassifier, CosineClassifier, SPNetClassifier
from .utils import get_scheduler, get_batch, MeanReduction


class Trainer:
    def __init__(self, task, device, logger, opts):
        self.logger = logger
        self.device = device
        self.task = task
        self.opts = opts
        self.novel_classes = self.task.get_n_classes()[-1]
        self.step = task.step
        self.need_model_old = task.step > 0 and (opts.loss_kd > 0)

        self.n_channels = -1  # features size, will be initialized in make model
        self.model = self.make_model()
        self.model = self.model.to(device)
        self.distributed = False
        self.model_old = None
        if self.need_model_old:
            self.model_old = self.make_model(is_old=True)
            # put the old model into distributed memory and freeze it
            for par in self.model_old.parameters():
                par.requires_grad = False
            self.model_old.to(device)
            self.model_old.eval()

        if opts.fix_bn:
            self.model.fix_bn()

        if opts.bn_momentum is not None:
            self.model.bn_set_momentum(opts.bn_momentum)

        # xxx Set up optimizer
        params = []
        if not opts.freeze:
            params.append({"params": filter(lambda p: p.requires_grad, self.model.body.parameters())})

        if opts.lr_head != 0:
            params.append({"params": filter(lambda p: p.requires_grad, self.model.head.parameters()),
                           'lr': opts.lr * opts.lr_head})

        if opts.method != "SPN":
            if opts.train_only_novel:
                params.append({"params": filter(lambda p: p.requires_grad, self.model.cls.cls[task.step].parameters()),
                               'lr': opts.lr * opts.lr_cls})
            else:
                params.append({"params": filter(lambda p: p.requires_grad, self.model.cls.parameters()),
                               'lr': opts.lr * opts.lr_cls})

        self.optimizer = torch.optim.SGD(params, lr=opts.lr, momentum=0.9, weight_decay=opts.weight_decay)
        self.scheduler = get_scheduler(opts, self.optimizer)
        self.logger.debug("Optimizer:\n%s" % self.optimizer)

        reduction = 'none'
        if opts.focal:
            self.criterion = FocalLoss(ignore_index=255, reduction=reduction)
        else:
            self.criterion = nn.CrossEntropyLoss(ignore_index=255, reduction=reduction)

        self.reduction = HardNegativeMining() if opts.hnm else MeanReduction()

        self.kd_crit = KnowledgeDistillationLoss(reduction="mean") if task.step > 0 and opts.loss_kd > 0 else None
        self.kd_weight = opts.loss_kd

        self.supp_reg = opts.supp_reg
        self.entropy_loss = None if self.supp_reg == 0 else EntropyLoss()

        self.initialize(opts)  # setup the model, optimizer, scheduler and criterion

    def make_model(self, is_old=False):
        classifier, self.n_channels = self.get_classifier(is_old)
        model = make_model(self.opts, classifier)
        return model

    def distribute(self):
        opts = self.opts
        if self.model is not None:
            # Put the model on GPU
            self.distributed = True
            self.model = DistributedDataParallel(self.model, device_ids=[opts.local_rank],
                                                 output_device=opts.local_rank)  # , find_unused_parameters=True)

    def get_classifier(self, is_old=False):
        # here distinguish methods!
        opts = self.opts
        if opts.method == "SPN":
            classes = self.task.get_old_labels() if is_old else self.task.get_order()
            cls = SPNetClassifier(opts, classes)
            n_feat = cls.channels
        elif opts.method == 'COS':
            n_feat = self.opts.n_feat
            n_classes = self.task.get_n_classes()[:-1] if is_old else self.task.get_n_classes()
            cls = CosineClassifier(n_classes, channels=n_feat)
        else:
            n_feat = self.opts.n_feat
            n_classes = self.task.get_n_classes()[:-1] if is_old else self.task.get_n_classes()
            cls = IncrementalClassifier(n_classes, channels=n_feat)
        return cls, n_feat

    def initialize(self, opts):
        pass

    def warm_up(self, dataset, epochs=1):
        pass

    def cool_down(self, dataset, epochs=1):
        pass

    def train(self, cur_epoch, train_loader, metrics=None, print_int=10, n_iter=1, supp_loader=None):
        """Train and return epoch loss"""
        if metrics is not None:
            metrics.reset()
        logger = self.logger
        optim = self.optimizer
        scheduler = self.scheduler
        logger.info("Epoch %d, lr = %f" % (cur_epoch, optim.param_groups[0]['lr']))

        device = self.device
        model = self.model
        criterion = self.criterion

        epoch_loss = 0.0
        reg_loss = 0.0
        interval_loss = 0.0

        model.train()
        if self.opts.freeze and self.opts.bn_momentum == 0:
            model.module.body.eval()
        if self.opts.lr_head == 0 and self.opts.bn_momentum == 0:
            model.module.head.eval()

        supp_iterator = iter(supp_loader) if supp_loader is not None else None

        cur_step = 0
        for iteration in range(n_iter):
            for images, labels in train_loader:

                images = images.to(device, dtype=torch.float32)
                labels = labels.to(device, dtype=torch.long)

                if supp_loader is not None:
                    supp_iterator, supp_batch = get_batch(supp_iterator, supp_loader)
                    supp_batch[0] = supp_batch[0].to(device)
                    images = torch.cat((images, supp_batch[0]), dim=0)

                rloss = torch.tensor([0.]).to(self.device)
                optim.zero_grad()
                outputs = model(images)

                if supp_loader is not None:
                    if self.entropy_loss is not None:
                        supp_out = outputs[-len(supp_batch[0]):]
                        ent_loss = self.entropy_loss(supp_out[:, 1:])
                        rloss += ent_loss * self.supp_reg
                    outputs = outputs[:-len(supp_batch[0])]  # remove support images from output

                loss = self.reduction(criterion(outputs, labels), labels)

                # xxx Distillation/Regularization Losses
                if self.model_old is not None:
                    outputs_old = self.model_old(images)
                    if self.kd_crit is not None:
                        kd_loss = self.kd_weight * self.kd_crit(outputs, outputs_old)
                        rloss += kd_loss

                loss_tot = loss + rloss
                loss_tot.backward()

                optim.step()
                scheduler.step()

                epoch_loss += loss.item()
                reg_loss += rloss.item()
                interval_loss += loss_tot.item()

                _, prediction = outputs.max(dim=1)  # B, H, W
                labels = labels.cpu().numpy()
                prediction = prediction.cpu().numpy()
                if metrics is not None:
                    metrics.update(labels, prediction)

                cur_step += 1
                if cur_step % print_int == 0:
                    interval_loss = interval_loss / print_int
                    logger.info(f"Epoch {cur_epoch}, Batch {cur_step}/{n_iter}*{len(train_loader)},"
                                f" Loss={interval_loss}")
                    logger.debug(f"Loss made of: CE {loss}")
                    # visualization
                    if logger is not None:
                        x = cur_epoch * len(train_loader) * n_iter + cur_step
                        logger.add_scalar('Loss', interval_loss, x)
                    interval_loss = 0.0

        # collect statistics from multiple processes
        epoch_loss = torch.tensor(epoch_loss).to(self.device)
        reg_loss = torch.tensor(reg_loss).to(self.device)

        torch.distributed.reduce(epoch_loss, dst=0)
        torch.distributed.reduce(reg_loss, dst=0)

        if distributed.get_rank() == 0:
            epoch_loss = epoch_loss / distributed.get_world_size() / (len(train_loader) * n_iter)
            reg_loss = reg_loss / distributed.get_world_size() / (len(train_loader) * n_iter)

        # collect statistics from multiple processes
        if metrics is not None:
            metrics.synch(device)

        logger.info(f"Epoch {cur_epoch}, Class Loss={epoch_loss}, Reg Loss={reg_loss}")

        return epoch_loss, reg_loss

    def validate(self, loader, metrics, ret_samples_ids=None, novel=False):
        """Do validation and return specified samples"""
        metrics.reset()
        model = self.model
        device = self.device
        criterion = self.criterion
        logger = self.logger

        class_loss = 0.0

        ret_samples = []
        with torch.no_grad():
            model.eval()
            for i, (images, labels) in enumerate(loader):

                images = images.to(device, dtype=torch.float32)
                labels = labels.to(device, dtype=torch.long)

                outputs = model(images)  # B, C, H, W
                if novel:
                    outputs[:, 1:-self.novel_classes] = -float("Inf")

                loss = criterion(outputs, labels).mean()

                class_loss += loss.item()

                _, prediction = outputs.max(dim=1)  # B, H, W
                labels = labels.cpu().numpy()
                prediction = prediction.cpu().numpy()
                metrics.update(labels, prediction)

                if ret_samples_ids is not None and i in ret_samples_ids:  # get samples
                    ret_samples.append((images[0].detach().cpu().numpy(),
                                        labels[0], prediction[0]))

            # collect statistics from multiple processes
            metrics.synch(device)

            class_loss = torch.tensor(class_loss).to(self.device)

            torch.distributed.reduce(class_loss, dst=0)

            if distributed.get_rank() == 0:
                class_loss = class_loss / distributed.get_world_size() / len(loader)

            if logger is not None:
                logger.info(f"Validation, Class Loss={class_loss}")

        return class_loss, ret_samples

    def load_state_dict(self, checkpoint, strict=True):
        state = {}
        if (self.need_model_old and not strict) or not self.distributed:
            for k, v in checkpoint["model"].items():
                state[k[7:]] = v
        state = state if not self.distributed else checkpoint['model']

        if self.need_model_old and not strict:
            self.model_old.load_state_dict(state, strict=True)  # we are loading the old model

        if 'module.cls.class_emb' in state and not strict:  # if distributed
            # remove from checkpoint since SPNClassifier is not incremental
            del state['module.cls.class_emb']

        if 'cls.class_emb' in state and not strict:  # if not distributed
            # remove from checkpoint since SPNClassifier is not incremental
            del state['cls.class_emb']

        model_state = state
        self.model.load_state_dict(model_state, strict=strict)

        if strict:  # if strict, we are in ckpt (not step) so load also optim and scheduler
            self.optimizer.load_state_dict(checkpoint["optimizer"])
            self.scheduler.load_state_dict(checkpoint["scheduler"])

    def state_dict(self):
        state = {"model": self.model.state_dict(), "optimizer": self.optimizer.state_dict(),
                 "scheduler": self.scheduler.state_dict()}
        return state