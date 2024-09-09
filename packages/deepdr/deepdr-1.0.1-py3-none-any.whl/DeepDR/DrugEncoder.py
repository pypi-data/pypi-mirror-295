import math
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import Set2Set
import torch_geometric.nn.models as models
from torch_geometric.nn.conv import GCNConv, GATConv

from ._TrimNet_model import Block
from ._MPG_model import MolGNet

_in_dim = 512
_drug_dim = 768
_dropout = 0.3

_num_embedding = 37
_kernel_size = 3
_padding = 1
_bidirectional = True

_x_num_embedding = 178
_edge_num_embedding = 18
_num_heads = 4

"""
DNN
input: [batch_size, in_dim]
output: [batch_size, ft_dim]
"""


class DNN(nn.Module):
    def __init__(self, in_dim: int, ft_dim: int, hid_dim: int = 512, num_layers: int = 2, dropout: float = _dropout):
        """hid_dim, num_layers"""
        super(DNN, self).__init__()
        assert num_layers >= 1
        dim_ls = [in_dim] + [hid_dim] * (num_layers - 1) + [ft_dim]
        self.encode = nn.ModuleList([nn.Linear(dim_ls[i], dim_ls[i + 1]) for i in range(num_layers - 1)])
        self.dropout = nn.ModuleList([nn.Dropout(p=dropout) for _ in range(num_layers - 1)])
        self.output = nn.Linear(dim_ls[-2], dim_ls[-1])

    def forward(self, f):
        for i in range(len(self.encode)):
            f = F.relu(self.encode[i](f))
            f = self.dropout[i](f)
        f = self.output(f)
        return f


"""
CNN GRU LSTM
input: preprocessed_SMILES [batch_size, seq_len]
output: encoded_SMILES [batch_size, ft_dim, seq_len]
"""


class CNN(nn.Module):
    def __init__(self, embedding: bool = True, num_embedding: int = _num_embedding, embedding_dim: int = 735,
                 hid_channel_ls: list = None, kernel_size_conv: int = 7, stride_conv: int = 1, padding_conv: int = 0,
                 kernel_size_pool: int = 3, stride_pool: int = 3, padding_pool: int = 0, batch_norm: bool = True,
                 max_pool: bool = True, flatten: bool = True, debug: bool = False):
        """tCNNS: let embedding=False batch_norm=False"""
        super(CNN, self).__init__()
        self.embedding = embedding
        self.num_embedding = num_embedding
        self.batch_norm = batch_norm
        self.max_pool = max_pool
        self.flatten = flatten
        self.debug = debug

        if hid_channel_ls is None:
            hid_channel_ls = [40, 80, 60]
        channel_ls = [embedding_dim if self.embedding else num_embedding] + hid_channel_ls

        if self.embedding:
            self.embed = nn.Embedding(num_embedding, embedding_dim)
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
        f = self.embed(f) if self.embedding else F.one_hot(f.to(torch.int64), self.num_embedding).float()
        f = f.permute(0, 2, 1).contiguous()

        for i in range(len(self.conv)):
            f = self.conv[i](f)
            if self.batch_norm:
                f = self.norm[i](f)
            f = F.relu(f)
            if self.max_pool:
                f = self.pool[i](f)

        if self.flatten:
            f = self.flat(f)

        if self.debug:
            print(f.shape)
        return f


class GRU(nn.Module):
    def __init__(self, num_embedding: int = _num_embedding, embedding_dim: int = _drug_dim, ft_dim: int = _drug_dim,
                 dropout: float = _dropout, bidirectional: bool = _bidirectional, num_layers: int = 2):
        """num_layers"""
        super(GRU, self).__init__()
        assert num_layers >= 1
        assert ft_dim % 2 == 0
        self.embedding = nn.Embedding(num_embedding, embedding_dim)
        self.encode_gru = torch.nn.GRU(input_size=embedding_dim, hidden_size=ft_dim // (2 if bidirectional else 1),
                                       num_layers=num_layers, dropout=dropout, bidirectional=bidirectional,
                                       batch_first=True)

    def forward(self, f):
        f = self.embedding(f)
        f, _ = self.encode_gru(f)
        f = f.permute(0, 2, 1).contiguous()
        return f


class LSTM(nn.Module):
    def __init__(self, num_embedding: int = _num_embedding, embedding_dim: int = _drug_dim, ft_dim: int = _drug_dim,
                 dropout: float = _dropout, bidirectional: bool = _bidirectional, num_layers: int = 2):
        """num_layers"""
        super(LSTM, self).__init__()
        assert num_layers >= 1
        assert ft_dim % 2 == 0
        self.embedding = nn.Embedding(num_embedding, embedding_dim)
        self.encode_lstm = torch.nn.LSTM(input_size=embedding_dim, hidden_size=ft_dim // (2 if bidirectional else 1),
                                         num_layers=num_layers, dropout=dropout, bidirectional=bidirectional,
                                         batch_first=True)

    def forward(self, f):
        f = self.embedding(f)
        f, _ = self.encode_lstm(f)
        f = f.permute(0, 2, 1).contiguous()
        return f


"""
GCN GAT MPG
input: preprocessed_Graph
output: encoded_Graph.x, preprocessed_Graph
"""


class GCN(nn.Module):
    def __init__(self, x_num_embedding: int = _x_num_embedding, embedding_dim: int = _drug_dim, ft_dim: int = _drug_dim,
                 hid_dim: int = 384, num_layers: int = 2):
        """hid_dim, num_layers"""
        super(GCN, self).__init__()
        assert num_layers >= 2
        self.x_embedding = nn.Embedding(x_num_embedding, embedding_dim)
        self.reset_parameters()
        self.input = GCNConv(embedding_dim, hid_dim)
        self.encode_gcn = nn.ModuleList([GCNConv(hid_dim, hid_dim) for _ in range(num_layers - 2)])
        self.output = GCNConv(hid_dim, ft_dim)

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.x_embedding.weight.data)

    def forward(self, g):
        x, edge_index = g.x, g.edge_index
        x = self.x_embedding(x).sum(1)
        x = F.relu(self.input(x, edge_index))
        for layer in self.encode_gcn:
            x = x + F.relu(layer(x, edge_index))
        x = self.output(x, edge_index)
        return x, g


class GAT(nn.Module):
    def __init__(self, x_num_embedding: int = _x_num_embedding, edge_num_embedding: int = _edge_num_embedding,
                 embedding_dim: int = _drug_dim, ft_dim: int = _drug_dim, num_heads: int = _num_heads,
                 dropout: float = _dropout, hid_dim: int = 384, num_layers: int = 2):
        """hid_dim num_layers"""
        super(GAT, self).__init__()
        assert num_layers >= 2
        self.x_embedding = nn.Embedding(x_num_embedding, embedding_dim)
        self.edge_embedding = nn.Embedding(edge_num_embedding, embedding_dim)
        self.reset_parameters()
        self.input = GATConv(embedding_dim, hid_dim, heads=num_heads, concat=False, edge_dim=embedding_dim,
                             dropout=dropout)
        self.encode_gat = nn.ModuleList(
            [GATConv(hid_dim, hid_dim, heads=num_heads, concat=False, edge_dim=embedding_dim, dropout=dropout)
             for _ in range(num_layers - 2)])
        self.output = GATConv(hid_dim, ft_dim, heads=num_heads, concat=False, edge_dim=embedding_dim)

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.x_embedding.weight.data)
        torch.nn.init.xavier_uniform_(self.edge_embedding.weight.data)

    def forward(self, g):
        x, edge_index, edge_attr = g.x, g.edge_index, g.edge_attr
        x = self.x_embedding(x).sum(1)
        edge_attr = self.edge_embedding(edge_attr).sum(1)
        x = F.relu(self.input(x, edge_index, edge_attr))
        for layer in self.encode_gat:
            x = x + F.relu(layer(x, edge_index, edge_attr))
        x = self.output(x, edge_index, edge_attr)
        return x, g


class MPG(nn.Module):
    def __init__(self, ft_dim: int = 768, MPG_dim: int = 768, freeze: bool = True, conv: bool = True,
                 num_layer=5, emb_dim=768, heads=12, num_message_passing=3, drop_ratio=0, pt_path=None):
        """"""
        super(MPG, self).__init__()
        if freeze is False:
            assert pt_path is not None
        self.freeze = freeze
        self.conv = conv
        if self.freeze is not True:
            self.net = MolGNet(num_layer=num_layer, emb_dim=emb_dim, heads=heads,
                               num_message_passing=num_message_passing, drop_ratio=drop_ratio)
            self.net.load_state_dict(torch.load(pt_path))
        if self.conv:
            self.output = GCNConv(MPG_dim, ft_dim)

    def forward(self, g):
        if self.freeze:
            x = g.mpg_ft
        else:
            x = self.net(g)
        if self.conv:
            x = self.output(x, g.edge_index)
        return x, g


"""
TrimNet AttentiveFP
input: preprocessed_Graph
output: drug_ft [batch_size, ft_dim]
"""


class TrimNet(nn.Module):
    def __init__(self, x_num_embedding: int = _x_num_embedding, edge_num_embedding: int = _edge_num_embedding,
                 embedding_dim: int = _drug_dim, ft_dim: int = 2, num_heads: int = 4, dropout: float = 0.1,
                 hid_dim: int = 32, depth: int = 3):
        """"""
        super(TrimNet, self).__init__()
        self.dropout = dropout
        self.x_embedding = nn.Embedding(x_num_embedding, embedding_dim)
        self.edge_embedding = nn.Embedding(edge_num_embedding, embedding_dim)
        self.reset_parameters()
        self.lin0 = nn.Linear(embedding_dim, hid_dim)
        self.convs = nn.ModuleList([Block(hid_dim, embedding_dim, num_heads) for _ in range(depth)])
        self.set2set = Set2Set(hid_dim, processing_steps=3)
        self.out = nn.Sequential(nn.Linear(2 * hid_dim, 512), nn.LayerNorm(512), nn.ReLU(inplace=True),
                                 nn.Dropout(p=self.dropout), nn.Linear(512, ft_dim))

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.x_embedding.weight.data)
        torch.nn.init.xavier_uniform_(self.edge_embedding.weight.data)

    def forward(self, g):
        x, edge_index, edge_attr, batch = g.x, g.edge_index, g.edge_attr, g.batch
        x = self.x_embedding(x).sum(1)
        edge_attr = self.edge_embedding(edge_attr).sum(1)
        x = F.celu(self.lin0(x))
        for conv in self.convs:
            x = x + F.dropout(conv(x, edge_index, edge_attr), p=self.dropout, training=self.training)
        x = self.set2set(x, batch)
        x = self.out(F.dropout(x, p=self.dropout, training=self.training))
        return x


class AttentiveFP(nn.Module):
    def __init__(self, x_num_embedding: int = _x_num_embedding, edge_num_embedding: int = _edge_num_embedding,
                 embedding_dim: int = _drug_dim, ft_dim: int = _drug_dim, dropout: float = _dropout,
                 hid_dim: int = 384, num_layers: int = 2, num_steps: int = 3):
        """hid_dim, num_layers, num_steps"""
        super(AttentiveFP, self).__init__()
        assert num_layers >= 1
        self.x_embedding = nn.Embedding(x_num_embedding, embedding_dim)
        self.edge_embedding = nn.Embedding(edge_num_embedding, embedding_dim)
        self.reset_parameters()
        self.encode_AttentiveFP = models.AttentiveFP(in_channels=embedding_dim, hidden_channels=hid_dim,
                                                     out_channels=ft_dim, edge_dim=embedding_dim, num_layers=num_layers,
                                                     num_timesteps=num_steps, dropout=dropout)

    def reset_parameters(self):
        torch.nn.init.xavier_uniform_(self.x_embedding.weight.data)
        torch.nn.init.xavier_uniform_(self.edge_embedding.weight.data)

    def forward(self, g):
        x, edge_index, edge_attr, batch = g.x, g.edge_index, g.edge_attr, g.batch
        x = self.x_embedding(x).sum(1)
        edge_attr = self.edge_embedding(edge_attr).sum(1)
        x = self.encode_AttentiveFP(x, edge_index, edge_attr, batch)
        return x


"""
Resnet18 ImageMol
input: preprocessed_Image
output: drug_ft [batch_size, ft_dim]
"""


class Resnet18(nn.Module):
    def __init__(self):
        super(Resnet18, self).__init__()
        model = torchvision.models.resnet18(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, 2)
        self.embedding_layer = nn.Sequential(*list(model.children())[:-1])
        self.jigsaw_classifier = nn.Linear(512, 101)
        self.class_classifier1 = nn.Linear(512, 100)
        self.class_classifier2 = nn.Linear(512, 1000)
        self.class_classifier3 = nn.Linear(512, 10000)
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2.0 / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        x = self.embedding_layer(x)
        x = x.view(x.size(0), -1)
        return x


class ImageMol(nn.Module):
    def __init__(self, pth_tar_path):
        super(ImageMol, self).__init__()
        self.net = Resnet18()
        self.net.load_state_dict(torch.load(pth_tar_path)['state_dict'], strict=False)

    def forward(self, x):
        return self.net(x)


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
