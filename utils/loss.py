import torch.nn as nn
import torch.nn.functional as F
import torch


class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, ignore_index=255, reduction="none"):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', ignore_index=self.ignore_index)
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1-pt)**self.gamma * ce_loss
        if self.reduction == "mean":
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss


class HardNegativeMining(nn.Module):
    def __init__(self, perc=0.25):
        super().__init__()
        self.perc = perc

    def forward(self, loss, target=None):
        # inputs should be B, H, W
        B = loss.shape[0]
        loss = loss.reshape(B, -1)
        P = loss.shape[1]
        tk = loss.topk(dim=1, k=int(self.perc*P))
        loss = tk[0].mean()
        return loss


class EntropyLoss(nn.Module):
    def __init__(self, reduction='mean'):
        super().__init__()
        self.reduction = reduction

    def forward(self, inputs):
        prob = torch.softmax(inputs, dim=1)
        log_prob = torch.log_softmax(inputs, dim=1)
        loss = (log_prob * prob).sum(dim=1)
        if self.reduction == 'mean':
            loss = torch.mean(loss)
        elif self.reduction == 'sum':
            loss = torch.sum(loss)
        return -loss


class KnowledgeDistillationLoss(nn.Module):
    def __init__(self, reduction='mean', alpha=1.):
        super().__init__()
        self.reduction = reduction
        self.alpha = alpha

    def forward(self, inputs, targets, mask=None):
        inputs = inputs.narrow(1, 0, targets.shape[1])

        outputs = torch.log_softmax(inputs, dim=1)
        labels = torch.softmax(targets * self.alpha, dim=1)

        loss = (outputs * labels).mean(dim=1)

        if mask is not None:
            loss = loss * mask.float()

        if self.reduction == 'mean':
            outputs = -torch.mean(loss)  # torch.masked_select(loss, mask).mean()
        elif self.reduction == 'sum':
            outputs = -torch.sum(loss)
        else:
            outputs = -loss

        return outputs


class UnbiasedKnowledgeDistillationLoss(nn.Module):
    def __init__(self, reduction='mean', alpha=1.):
        super().__init__()
        self.reduction = reduction
        self.alpha = alpha

    def forward(self, inputs, targets, mask=None):

        new_cl = inputs.shape[1] - targets.shape[1]

        targets = targets * self.alpha

        new_bkg_idx = torch.tensor([0] + [x for x in range(targets.shape[1], inputs.shape[1])]).to(inputs.device)

        den = torch.logsumexp(inputs, dim=1)                          # B, H, W
        outputs_no_bgk = inputs[:, 1:-new_cl] - den.unsqueeze(dim=1)  # B, OLD_CL, H, W
        outputs_bkg = torch.logsumexp(torch.index_select(inputs, index=new_bkg_idx, dim=1), dim=1) - den     # B, H, W

        labels = torch.softmax(targets, dim=1)                        # B, BKG + OLD_CL, H, W

        # make the average on the classes 1/n_cl \sum{c=1..n_cl} L_c
        loss = (labels[:, 0] * outputs_bkg + (labels[:, 1:] * outputs_no_bgk).sum(dim=1)) / targets.shape[1]

        if mask is not None:
            loss = loss * mask.float()

        if self.reduction == 'mean':
            outputs = -torch.mean(loss)
        elif self.reduction == 'sum':
            outputs = -torch.sum(loss)
        else:
            outputs = -loss

        return outputs


class WeightRegularizationLoss(nn.Module):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes

    @staticmethod
    def cosine(x, y):
        return (F.normalize(x, dim=0)*F.normalize(y, dim=0)).sum()

    def forward(self, model, distributed=True):
        cls = model.module.cls.cls if distributed else model.cls.cls
        loss = 0.
        for i in range(self.classes[-1]):
            loss += self.cosine(cls[0].weight[0], cls[-1].weight[i])
        return loss / self.classes[-1]
