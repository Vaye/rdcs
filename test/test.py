# -*- coding: utf-8 -*-

'''
Author: Jiawei Ye
Date: 2023-06-19 21:18:55
LastEditors: Jiawei Ye
LastEditTime: 2023-08-08 22:46:06
FilePath: /rdcs/test/test.py
Description: 

'''
import requests
import json
# from swissknife import show_all_plots, plot_from_dict
# import matplotlib.pyplot as plt
import base64
import io
import os
from PIL import Image
# plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取json文件
print(os.getcwd())
with open('test/gd2b_livetest.json', 'r') as f:
    data = json.load(f)

target_ip = os.getenv('TARGET_IP', '127.0.0.1')
# 发送POST请求
response = requests.post(f'http://{target_ip}:4999/main', json=data)

# 将返回结果转为json
result = response.json()

# 获取需要的值
anomaly = result.get('anomaly')
cl_plots = result.get('cl_plots')
kpi_plots = result.get('kpi_plots')

print(kpi_plots.keys())

# def show_all_plots(all_plots):
#     for ne, plot_data in all_plots.items():
#         # Decode the Base64 string to bytes
#         image_bytes = base64.b64decode(plot_data)

#         # Read the bytes as an image
#         image = Image.open(io.BytesIO(image_bytes))

#         # Display the image
#         plt.figure(figsize=(10, 10))
#         plt.imshow(image)
#         plt.title(ne)
#         plt.axis('off')  # Hide the axis
#         plt.savefig(f'output/NE_{ne}.png')
#         plt.close()

# def plot_from_dict(result_dict):
#     for ne, kpi_dict in result_dict.items():
#         for kpi, image_base64 in kpi_dict.items():
#             image_bytes = base64.b64decode(image_base64)
#             image = Image.open(io.BytesIO(image_bytes))
            
#             plt.figure(figsize=(10, 5))
#             plt.title(f'neName: {ne} - KPI: {kpi}')
#             # plt.imshow(image)
#             plt.axis('off')  # disable axis
#             plt.savefig(f'output/NE_{ne}_KPI_{kpi}.png')
#             plt.close()

# show_all_plots(cl_plots)

# plot_from_dict(kpi_plots)

def save_xcode_fig(xcode_image_dict):
    for ne, plot_data in xcode_image_dict.items():
        # Decode the Base64 string to bytes
        image_bytes = base64.b64decode(plot_data)

        filename = f'output/NE_{ne}.png'
        with open(filename, 'wb') as f:
            f.write(image_bytes)

def save_kpi_fig(kpi_image_dict):
    for ne, kpi_dict in kpi_image_dict.items():
        for kpi, image_base64 in kpi_dict.items():
            image_bytes = base64.b64decode(image_base64)

            filename = f'output/NE_{ne}_KPI_{kpi}.png'
            with open(filename, 'wb') as f:
                f.write(image_bytes)

save_xcode_fig(cl_plots)

save_kpi_fig(kpi_plots)
