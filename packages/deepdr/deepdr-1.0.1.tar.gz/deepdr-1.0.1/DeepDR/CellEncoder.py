"""
DNN CNN DAE NULL
input: exp, pes, mut or cnv [batch_size, in_dim]
output: cell_ft [batch_size, cell_dim]
"""

import os
import torch
from torch import nn
import torch.nn.functional as F

from ._DAE_pretrain import PretrainDAE


class DNN(nn.Module):
    def __init__(self, in_dim: int, ft_dim: int, hid_dim: int = 100, num_layers: int = 2, dropout: float = 0.3):
        """hid_dim, num_layers"""
        super(DNN, self).__init__()
        assert num_layers >= 1
        dim_ls = [in_dim] + [hid_dim] * (num_layers - 1) + [ft_dim]
        self.encode_dnn = nn.ModuleList([nn.Linear(dim_ls[i], dim_ls[i + 1]) for i in range(num_layers - 1)])
        self.dropout = nn.ModuleList([nn.Dropout(p=dropout) for _ in range(num_layers - 1)])
        self.output = nn.Linear(dim_ls[-2], dim_ls[-1])

    def forward(self, f):
        for i in range(len(self.encode_dnn)):
            f = F.relu(self.encode_dnn[i](f))
            f = self.dropout[i](f)
        f = self.output(f)
        return f


class CNN(nn.Module):
    def __init__(self, in_dim: int, ft_dim: int = 735, hid_channel_ls: list = None, kernel_size_conv: int = 7,
                 stride_conv: int = 1, padding_conv: int = 0, kernel_size_pool: int = 3, stride_pool: int = 3,
                 padding_pool: int = 0, batch_norm: bool = True, max_pool: bool = True, flatten: bool = True,
                 debug: bool = False):
        """tCNNS: let batch_norm=False"""
        super(CNN, self).__init__()
        self.batch_norm = batch_norm
        self.max_pool = max_pool
        self.flatten = flatten
        self.debug = debug

        if hid_channel_ls is None:
            hid_channel_ls = [40, 80, 60]
        channel_ls = [1] + hid_channel_ls

        self.input = nn.Linear(in_dim, ft_dim)
        self.conv = nn.ModuleList([nn.Conv1d(in_channels=channel_ls[i], out_channels=channel_ls[i + 1],
                                             kernel_size=kernel_size_conv, stride=stride_conv, padding=padding_conv)
                                   for i in range(len(channel_ls) - 1)])
        if self.batch_norm:
            self.norm = nn.ModuleList([nn.BatchNorm1d(channel_ls[i + 1]) for i in range(len(channel_ls) - 1)])
        if self.max_pool:
            self.pool = nn.ModuleList([nn.MaxPool1d(kernel_size=kernel_size_pool, stride=stride_pool,
                                                    padding=padding_pool) for _ in range(len(channel_ls) - 1)])
        if self.flatten:
            self.flat = nn.Flatten()

    def forward(self, f):
        f = F.relu(self.input(f))
        f = torch.unsqueeze(f, dim=1)

        for i in range(len(self.conv)):
            f = self.conv[i](f)
            if self.batch_norm:
                f = self.norm[i](f)
            f = F.relu(f)
            if self.max_pool:
                f = self.pool[i](f)

        if self.flatten is False:
            f_mean = torch.mean(f, dim=1)
            f_max, _ = torch.max(f, dim=1)
            f_mix, _ = torch.min(f, dim=1)
            f = f_mean + f_max + f_mix
        else:
            f = self.flat(f)

        if self.debug:
            print(f.shape)
        return f


class DAE(nn.Module):
    def __init__(self, subset: bool = True, path: str = None):
        """"""
        super(DAE, self).__init__()
        if subset:
            self.encoder = DNN(in_dim=6163, ft_dim=100)
            self.encoder.load_state_dict(torch.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/DAE.pt')))
            # self.decoder = DNN(in_dim=100, ft_dim=6163)
        else:
            assert path is not None
            self.encoder = DNN(in_dim=17420, hid_dim=512, num_layers=3, ft_dim=100)
            self.encoder.load_state_dict(torch.load(path))
            # self.decoder = DNN(in_dim=100, ft_dim=17420)

    def forward(self, f):
        return self.encoder(f)


"""
NULL
input == output
"""


class NULL(nn.Module):
    def __init__(self):
        """"""
        super(NULL, self).__init__()

    def forward(self, f):
        return f
