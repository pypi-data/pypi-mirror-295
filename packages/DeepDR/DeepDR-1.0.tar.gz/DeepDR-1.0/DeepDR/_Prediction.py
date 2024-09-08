import time
import pandas as pd
import torch.nn as nn

from .Data import DrDataset, DrDataLoader
from ._Training import device, _InferenceTP, _Inference


def Predict(model, data, save_path_prediction: str = None):
    for i in range(len(data)):
        data.pair_ls[i] += [0.0] if len(data.pair_ls[i]) == 2 else []
    data_loader = DrDataLoader(DrDataset(data), batch_size=64, shuffle=False)
    result = Eval(model, data_loader, no_tag=True, save_path_prediction=save_path_prediction)
    return result


def Eval(model, data_loader, no_tag: bool = False, loss_func=None, classify: bool = False,
         save_path_prediction: str = None):
    """"""
    if save_path_prediction is not None:
        assert save_path_prediction[-4:] == '.csv'
    cell_encoder, drug_encoder, fusion_module = None, None, None
    if type(model) == tuple:
        cell_encoder, drug_encoder, fusion_module = model
        cell_encoder = cell_encoder.to(device)
        drug_encoder = drug_encoder.to(device)
        fusion_module = fusion_module.to(device)
    else:
        model = model.to(device)
    if loss_func is None:
        if not classify:
            loss_func = nn.MSELoss()
        else:
            loss_func = nn.BCEWithLogitsLoss()
    real_pre_dict = dict()
    print('Start prediction!')
    start = time.time()
    if type(model) == tuple:
        epoch_loss, real, pre, cell_ls, drug_ls = _InferenceTP(cell_encoder, drug_encoder, fusion_module, data_loader, loss_func)
    else:
        epoch_loss, real, pre, cell_ls, drug_ls = _Inference(model, data_loader, loss_func)
    if not no_tag:
        print('loss {:.6f}'.format(epoch_loss), end='  ')
    if save_path_prediction is not None:
        real_pre_dict['cell'] = cell_ls
        real_pre_dict['drug'] = drug_ls
        if not no_tag:
            real_pre_dict['real'] = real
        real_pre_dict['pre'] = pre
        dataframe = pd.DataFrame(real_pre_dict)
        dataframe.to_csv(save_path_prediction, index=False, sep=',')
    end = time.time()
    print('time consumed {:.6f}'.format(end - start))
    print('Prediction completed!')
    if not no_tag:
        return epoch_loss, real, pre, cell_ls, drug_ls
    else:
        return pre, cell_ls, drug_ls
