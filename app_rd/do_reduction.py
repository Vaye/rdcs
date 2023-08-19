# -*- coding: utf-8 -*-

'''
Author: Jiawei Ye
Date: 2023-06-19 21:18:55
LastEditors: Jiawei Ye
LastEditTime: 2023-08-19 11:23:59
FilePath: /rdcs_9sky/app_rd/do_reduction.py
Description: 

'''

from model import Autoencoder
import torch

class Reducer():
    def __init__(self, model_path, device, input_dim) -> None:
        self.device = device
        self.model_path = model_path
        self.model = Autoencoder(input_dim, xcode_dim=3, with_bn=True)
        self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device(self.device)))
        # self.model.load_state_dict(torch.load(self.model_path))
        self.model.to(self.device)
        self.model.eval()
        

    def reduction(self, data):
        x = torch.tensor(data, dtype=torch.float32)
        with torch.no_grad():
            y = self.model.encoder(x.to(self.device)).cpu()
        return y.numpy().tolist() #return xcode list