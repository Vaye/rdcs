# -*- coding: utf-8 -*-

'''
Author: Jiawei Ye
Date: 2023-06-19 21:18:55
LastEditors: Jiawei Ye
LastEditTime: 2023-06-20 21:49:29
FilePath: /rdcs/app_main/app_main.py
Description: 

'''

from flask import Flask, request, jsonify
import pandas as pd
from pandas import json_normalize
import requests
from retrying import retry
from swissknife import preprocess_data, tree_convert_dataframe_to_dict_and_ndarray_to_list_format
import logging
import json
import os


APP_RD = os.environ.get('APP_RD') or 'app_rd'
APP_CL = os.environ.get('APP_CL') or 'app_cl'
APP_PLOT = os.environ.get('APP_PLOT') or 'app_plot'

app = Flask(__name__)

# 初始化日志记录器
logging.basicConfig(filename='main_service.log', level=logging.INFO)

# 定义重试条件: 只有当特定异常被抛出时，才进行重试
def retry_if_connection_error(exception):
    return isinstance(exception, requests.exceptions.RequestException)

@retry(retry_on_exception=retry_if_connection_error, stop_max_attempt_number=3)
def send_request(url, data):
    try:
        response = requests.post(url, json=data, timeout=60)
        response.raise_for_status()  # 如果响应的状态码不是 200，引发异常
    except requests.exceptions.RequestException as e:
        logging.error("请求失败: %s", e)
        raise
    else:
        return response.json()

@app.route('/main', methods=['POST'])
def main_service():
    # 验证输入数据
    try:
        data = request.get_json()
        rawdata = pd.DataFrame(data['rawdata'])
        vendor = data['vendor']
        version = data['version']
        
    except Exception as e:
        logging.error("输入数据验证失败: %s", e)
        return jsonify({"error": "Invalid input data"}), 400
    
    # 对原始数据进行处理，得到 ds_norm， vendor，ne_time
    df_clean_df, df_ne_time_df, ds = preprocess_data(rawdata) #df df list
    ds_norm = tree_convert_dataframe_to_dict_and_ndarray_to_list_format(ds)
    # 发送请求到app_rd
    rd_url = f'http://{APP_RD}:5001/dimreduction'
    # rd_url = 'http://localhost:5001/dimreduction'
    xcode = send_request(rd_url, {'ds_norm': ds_norm})['xcode'] #input list output xcode list


    # 发送请求到app_cl
    cl_url = f'http://{APP_CL}:5002/cluster'
    # cl_url = 'http://localhost:5002/cluster'
    df_clean = df_clean_df.to_dict(orient='records')
    df_ne_time = df_ne_time_df.to_dict(orient='records')
    cl_data = send_request(cl_url, {'rawdata': df_clean, 'xcode': xcode, 'ne_time': df_ne_time})
    anomaly, xcode_dict, label_dict, anomaly_time_dict = cl_data['anomaly'], cl_data['xcode'], cl_data['label'], cl_data['anomaly_time']

    # 发送请求到app_plot
    plot_url = f'http://{APP_PLOT}:5003/plot'
    # plot_url = 'http://localhost:5003/plot'    
    plot_data = send_request(plot_url, {'rawdata': df_clean, 'xcode': xcode_dict, 'label': label_dict, 'anomaly_time': anomaly_time_dict})
    cl_plots, kpi_plots = plot_data['cl'], plot_data['kpi']

    # 返回最终的结果
    result = {
        'anomaly': anomaly, 
        'cl_plots': cl_plots, 
        'kpi_plots': kpi_plots
        }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4999, threaded=True)
