# -*- coding: utf-8 -*-

'''
Author: Jiawei Ye
Date: 2023-08-18 16:13:10
LastEditors: Jiawei Ye
LastEditTime: 2023-08-19 12:09:42
FilePath: /rdcs_9sky/app_rd/app_rd.py
Description: 

'''
import logging
import os
from time import sleep, time

import joblib
import numpy as np
import torch
from do_reduction import Reducer
from flask import Flask, jsonify, request

INPUT_DIM = int(os.environ.get("INPUT_DIM"))
MODEL_PATH_NAME = os.environ.get("MODEL_PATH_NAME")

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='rd_service.log', level=logging.INFO)


device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
reducer = Reducer(MODEL_PATH_NAME, device, INPUT_DIM)

@app.route('/dimreduction', methods=['POST'])
def dimreduction():
    try:
        data = request.get_json(force=True)
        ds = np.array(data["ds_norm"])
        # 对数据进行归一化
        scaler = joblib.load('/app/models/scaler.save')
        ds_norm=scaler.transform(ds).tolist()
        xcode = reducer.reduction(ds_norm)
        result = {'xcode':xcode} #list
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 400
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
