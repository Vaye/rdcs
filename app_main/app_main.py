# -*- coding: utf-8 -*-

"""
Author: Jiawei Ye
Date: 2023-06-19 21:18:55
LastEditors: Jiawei Ye
LastEditTime: 2023-08-18 18:03:17
FilePath: /rdcs_9sky/app_main/app_main.py
Description: 

"""

import json
import logging
import os

import pandas as pd
import requests
from flask import Flask, jsonify, request
from pandas import json_normalize
from report import report_service
from report.collector import ReportCollector
from retrying import retry
from swissknife import (
    preprocess_data,
    tree_convert_dataframe_to_dict_and_ndarray_to_list_format,
)

APP_RD = os.environ.get("APP_RD") or "app_rd"
APP_CL = os.environ.get("APP_CL") or "app_cl"
APP_PLOT = os.environ.get("APP_PLOT") or "app_plot"

app = Flask(__name__)

# 初始化日志记录器
logging.basicConfig(filename="main_service.log", level=logging.INFO)


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


@app.route("/main", methods=["POST"])
def main_service():
    # for 9sky:创建一个 ReportCollector 实例，并设置 URL 和请求头参数
    param = (
        ReportCollector.url("/main", False)
        .header_param(request.headers.get("ability_invoking_param"))
        .multi_param(request.get_json())
    )
    # 验证输入数据
    try:
        data = request.get_json()
        rawdata = pd.DataFrame(data["rawdata"])
        vendor = data["vendor"]
        version = data["version"]
        # for 9sky:将请求中的参数收集到 ReportCollector 实例中
        param.multi_param(data)
    except Exception as e:
        logging.error("输入数据验证失败: %s", e)
        # for 9sky:如果出现异常，将成功标记设置为 False，响应代码设置为 400，并输出错误信息
        param.is_success(False).response_code(400).output_data(
            {"error": "Invalid input data"}
        )
        # for 9sky:记录请求信息
        report_service.report(param)
        return jsonify({"error": "Invalid input data"}), 400

    # 对原始数据进行处理，得到 ds_norm， vendor，ne_time
    df_clean_df, df_ne_time_df, ds = preprocess_data(rawdata)  # df df list
    ds_norm = tree_convert_dataframe_to_dict_and_ndarray_to_list_format(ds)
    # 发送请求到app_rd
    rd_url = f"http://{APP_RD}:5001/dimreduction"
    # rd_url = 'http://localhost:5001/dimreduction'
    xcode = send_request(rd_url, {"ds_norm": ds_norm})[
        "xcode"
    ]  # input list output xcode list

    # 发送请求到app_cl
    cl_url = f"http://{APP_CL}:5002/cluster"
    # cl_url = 'http://localhost:5002/cluster'
    df_clean = df_clean_df.to_dict(orient="records")
    df_ne_time = df_ne_time_df.to_dict(orient="records")
    cl_data = send_request(
        cl_url, {"rawdata": df_clean, "xcode": xcode, "ne_time": df_ne_time}
    )
    anomaly, xcode_dict, label_dict, anomaly_time_dict = (
        cl_data["anomaly"],
        cl_data["xcode"],
        cl_data["label"],
        cl_data["anomaly_time"],
    )

    # 发送请求到app_plot
    plot_url = f"http://{APP_PLOT}:5003/plot"
    # plot_url = 'http://localhost:5003/plot'
    plot_data = send_request(
        plot_url,
        {
            "rawdata": df_clean,
            "xcode": xcode_dict,
            "label": label_dict,
            "anomaly_time": anomaly_time_dict,
        },
    )
    cl_plots, kpi_plots = plot_data["cl"], plot_data["kpi"]

    # 返回最终的结果
    result = {"anomaly": anomaly, "cl_plots": cl_plots, "kpi_plots": kpi_plots}
    # for 9sky:如果一切正常，将成功标记设置为 True，响应代码设置为 200，并输出结果
    param.is_success(True).response_code(200).output_data(result)
    # for 9sky:记录请求信息
    report_service.report(param)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, threaded=True)
