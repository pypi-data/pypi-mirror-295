import os
import time
import torch
import joblib
import numpy as np
from rdkit import Chem
import pubchempy as pcp
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from torch.utils.data import Dataset
import torchvision.transforms as transforms

from ._MPG_model import MolGNet
from ._MPG_util import Self_loop, Add_seg_id
from ._MPG_loader import mol_to_graph_data_obj_complex

_char_ls = ["7", "6", "o", "]", "3", "s", "(", "-", "S", "/", "B", "4", "[", ")", "#", "I", "l", "O", "H", "c", "t", "1", "@",
            "=", "n", "P", "8", "C", "2", "F", "5", "r", "N", "+", "\\", ".", " "]
_max_len = 230

_Self_loop = Self_loop()
_Add_seg_id = Add_seg_id()


def _GetEcfp(smiles: str, radius: int = 2, nBits: int = 512):
    """"""
    mol = AllChem.MolFromSmiles(smiles)
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=radius, nBits=nBits)
    ECFP = np.zeros((nBits,), dtype=int)
    on_bits = list(fp.GetOnBits())
    ECFP[on_bits] = 1
    return ECFP.tolist()


def PreEcfp(smiles: str, radius: int = 2, nBits: int = 512):
    """"""
    smiles = AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True)
    return torch.tensor(_GetEcfp(smiles, radius, nBits), dtype=torch.float32)


def _PadSmiles(smiles: str, max_len: int = None, right: bool = True):
    """"""
    if max_len is None:
        max_len = _max_len
    assert max_len >= len(smiles)
    if right:
        return smiles + " " * (max_len - len(smiles))
    else:
        return " " * (max_len - len(smiles)) + smiles


def PreSmiles(smiles: str, max_len: int = None, char_dict: dict = None, right: bool = True):
    """"""
    if char_dict is None:
        char_dict = dict(zip(_char_ls, [i for i in range(len(_char_ls))]))
    smiles = _PadSmiles(AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True), max_len, right)
    return torch.tensor([char_dict[c] for c in smiles], dtype=torch.int)


def PreGraph(smiles: str):
    """"""
    smiles = AllChem.MolToSmiles(AllChem.MolFromSmiles(smiles), isomericSmiles=True, canonical=True)
    return _Add_seg_id(_Self_loop(mol_to_graph_data_obj_complex(AllChem.MolFromSmiles(smiles))))


class ImageDataset(Dataset):
    def __init__(self, smiles_ls):
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                              std=[0.229, 0.224, 0.225])
        self.transform = transforms.Compose([transforms.CenterCrop(224),
                                             transforms.ToTensor()])
        self.img_ls, self.smiles_err = self.smiles2img(smiles_ls)

    def __getitem__(self, index):
        return self.img_ls[index]

    def __len__(self):
        return len(self.img_ls)

    def smiles2img(self, smiles_ls):
        img_ls = []
        smiles_err = []
        for smiles in smiles_ls:
            try:
                mol = Chem.MolFromSmiles(smiles)
                img = Draw.MolsToGridImage([mol], molsPerRow=1, subImgSize=(224, 224))
                img_ls.append(self.normalize(self.transform(img.convert('RGB'))))
            except:
                smiles_err.append(smiles)
        if len(smiles_err) != 0:
            print("smiles error: {}".format(len(smiles_err)))
        return img_ls, smiles_err


def GetSMILESDict(pair_list: list, save: bool = True, save_path_SMILES_dict: str = None):
    """"""
    if save_path_SMILES_dict is None:
        t = time.localtime()
        save_path_SMILES_dict = 'SMILES_dict_{}_{}_{}_{}_{}_{}.pkl'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    print('Retrieving SMILES strings...')
    drug_list = sorted(list(set([each[1] for each in pair_list])))
    SMILES_dict_0 = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/SMILES_dict.pkl'))
    SMILES_dict = dict()
    SMILES_not_found = []
    for each in drug_list:
        if each in SMILES_dict_0:
            SMILES_dict[each] = SMILES_dict_0[each]
        else:
            try:
                _ = pcp.get_compounds(each, 'name')
                SMILES_dict[each] = _[0].isomeric_smiles
            except:
                SMILES_not_found.append(each)
    if save:
        joblib.dump(SMILES_dict, save_path_SMILES_dict)
    print('Total: {}  Successful: {}'.format(len(drug_list), len(drug_list) - len(SMILES_not_found)))
    return SMILES_dict


def GetMPGDict(SMILES_dict: dict, save: bool = True, save_path_MPG_dict: str = None):
    """"""
    if save_path_MPG_dict is None:
        t = time.localtime()
        save_path_MPG_dict = 'MPG_dict_{}_{}_{}_{}_{}_{}.pkl'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    MPG_dict_0 = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/MPG_dict.pkl'))
    MPG_dict = dict()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    gnn = MolGNet(num_layer=5, emb_dim=768, heads=12, num_message_passing=3, drop_ratio=0)
    gnn.load_state_dict(torch.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/MolGNet.pt')))
    gnn = gnn.to(device)
    gnn.eval()
    with torch.no_grad():
        for each in SMILES_dict:
            if each in MPG_dict_0:
                MPG_dict[each] = MPG_dict_0[each]
            else:
                graph = PreGraph(SMILES_dict[each]).to(device)
                MPG_dict[each] = gnn(graph).cpu()
    if save:
        joblib.dump(MPG_dict, save_path_MPG_dict)
    return MPG_dict


def GetGeneList():
    """"""
    f = open(os.path.join(os.path.split(__file__)[0], 'DefaultData/key.genes.txt'), encoding='gbk')
    Gene_list = []
    for each_row in f:
        Gene_list.append(each_row.strip())
    return Gene_list


def GetDefaultData(file_name: str, save: bool = False, save_path: str = None):
    """"""
    assert file_name in ['DAE.pt', 'DAE_ALL.pt', 'GDSC_CNV.pkl', 'GDSC_EXP.pkl', 'GDSC_MUT.pkl', 'GDSC_PES.pkl',
                         'MPG_dict.pkl', 'SMILES_dict.pkl', 'SMILESVec_dict.pkl', 'VAE_dict.pkl']
    file = joblib.load(os.path.join(os.path.split(__file__)[0], 'DefaultData/' + file_name))
    if save:
        save_path = file_name if save_path is None else save_path
        joblib.dump(file, save_path)
    return file
