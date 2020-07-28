from torch import nn
import torch
import pickle
from torch.nn import functional as F
import numpy as np
from torch.nn import Parameter


class IncrementalClassifier(nn.Module):
    def __init__(self, channels, classes, norm_feat=False):
        super().__init__()
        self.cls = nn.ModuleList(
            [nn.Conv2d(channels, c, 1) for c in classes])
        self.norm_feat = norm_feat

    def forward(self, x):
        if self.norm_feat:
            x = F.normalize(x, p=2, dim=1)
        out = []
        for mod in self.cls:
            out.append(mod(x))
        return torch.cat(out, dim=1)

    def imprint_weights(self, step, features):
        self.cls[step].weight.data = features.view_as(self.cls[step].weight.data)


class CosineClassifier(nn.Module):
    def __init__(self, channels, classes):
        super().__init__()
        self.cls = nn.ModuleList(
            [nn.Conv2d(channels, c, 1, bias=False) for c in classes])
        self.scaler = 10.

    def forward(self, x):
        x = F.normalize(x, p=2, dim=1)
        out = []
        for i, mod in enumerate(self.cls):
            out.append(self.scaler * F.conv2d(x, F.normalize(mod.weight, dim=1, p=2)))
        return torch.cat(out, dim=1)

    def imprint_weights(self, step, features):
        self.cls[step].weight.data = features.view_as(self.cls[step].weight.data)


class SPNetClassifier(nn.Module):
    def __init__(self, opts, classes):
        super().__init__()
        datadir = f"data/{opts.dataset}"
        if opts.embedding == 'word2vec':
            class_emb = pickle.load(open(datadir + '/word_vectors/word2vec.pkl', "rb"))
        elif opts.embedding == 'fasttext':
            class_emb = pickle.load(open(datadir + '/word_vectors/fasttext.pkl', "rb"))
        elif opts.embedding == 'fastnvec':
            class_emb = np.concatenate([pickle.load(open(datadir + '/word_vectors/fasttext.pkl', "rb")),
                                        pickle.load(open(datadir + '/word_vectors/word2vec.pkl', "rb"))], axis=1)
        else:
            raise NotImplementedError(f"Embeddings type {opts.embeddings} is not known")

        self.class_emb = class_emb[classes]
        self.class_emb = F.normalize(torch.tensor(self.class_emb), p=2, dim=1)
        self.class_emb = torch.transpose(self.class_emb, 1, 0).float()
        self.class_emb = Parameter(self.class_emb, False)
        self.in_channels = self.class_emb.shape[0]

    def forward(self, x):
        return torch.matmul(x.permute(0, 2, 3, 1), self.class_emb).permute(0, 3, 1, 2)