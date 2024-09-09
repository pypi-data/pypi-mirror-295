import os
import torch
import random
import joblib
import numpy as np
from abc import ABC
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def SetSeed(seed: int):
    """"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


class CollateFn:
    """"""
    def __init__(self):
        pass

    def __call__(self, batch):
        batch_data = torch.stack(batch)
        return batch_data


class MyDataSet(Dataset, ABC):
    """"""
    def __init__(self, data):
        self._data = data

    def __getitem__(self, idx):
        data = self._data[idx]
        return data

    def __len__(self):
        return len(self._data)


def PretrainDAE(data: str or dict, encoder, decoder, batch_size: int = 512, lr: float = 1e-4,
                epochs: int = 5000, seed: int = 1, noising: bool = True, save_path_encoder='DAE.pt',
                save_path_log=None, save_path_model=None):

    if type(data) == str:
        assert data in ['GDSC_CNV.pkl', 'GDSC_EXP.pkl', 'GDSC_MUT.pkl', 'GDSC_PES.pkl']
        data = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/' + data))

    GEF = []
    Cells = list(data.keys())
    for each in Cells:
        GEF.append(torch.tensor(data[each]))

    SetSeed(seed)
    encoder = encoder.to(device)
    decoder = decoder.to(device)
    loss_func = nn.MSELoss()
    params = [
        {'params': encoder.parameters()},
        {'params': decoder.parameters()}
    ]
    optimizer = optim.Adam(params, lr=lr)

    my_collate = CollateFn()
    train_loader = DataLoader(MyDataSet(GEF), batch_size=batch_size, shuffle=True, collate_fn=my_collate)

    for epoch in range(epochs):
        encoder.train()
        decoder.train()
        epoch_loss = 0
        it = 0
        for it, Ft in enumerate(train_loader):
            Ft = Ft.to(device)
            if noising:
                z = Ft.clone()
                y = np.random.binomial(1, 0.2, (z.shape[0], z.shape[1]))
                z[np.array(y, dtype=bool)] = 0
                Ft.requires_grad_(True)
                output = decoder(encoder(z))
            else:
                output = decoder(encoder(Ft))
            loss = loss_func(output, Ft)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.detach().item()

        epoch_loss /= (it + 1)
        if epoch % 10 == 9:
            print('Epoch {}, loss {:.6f}'.format(epoch, epoch_loss))
            if save_path_log is not None:
                with open(save_path_log, 'a') as file0:
                    print('Epoch {}, loss {:.6f}'.format(epoch, epoch_loss), file=file0)

        if epoch % 1000 == 999:
            if save_path_model is not None:
                joblib.dump((encoder, decoder), save_path_model)
            torch.save(encoder.state_dict(), save_path_encoder)
