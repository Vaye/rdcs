import requests
import json
# from swissknife import show_all_plots, plot_from_dict
import matplotlib.pyplot as plt
import base64
import io
from PIL import Image
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取json文件
with open('request1.json', 'r') as f:
    data = json.load(f)

# 发送POST请求
response = requests.post('http://127.0.0.1:4999/main', json=data)

# 将返回结果转为json
result = response.json()

# 获取需要的值
anomaly = result.get('anomaly')
cl_plots = result.get('cl_plots')
kpi_plots = result.get('kpi_plots')

def show_all_plots(all_plots):
    for ne, plot_data in all_plots.items():
        # Decode the Base64 string to bytes
        image_bytes = base64.b64decode(plot_data)

        # Read the bytes as an image
        image = Image.open(io.BytesIO(image_bytes))

        # Display the image
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        plt.title(ne)
        plt.axis('off')  # Hide the axis
        plt.show()

def plot_from_dict(result_dict):
    for ne, kpi_dict in result_dict.items():
        for kpi, image_base64 in kpi_dict.items():
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes))
            
            plt.figure(figsize=(10, 5))
            plt.title(f'neName: {ne} - KPI: {kpi}')
            plt.imshow(image)
            plt.axis('off')  # disable axis
            plt.show()

show_all_plots(cl_plots)

plot_from_dict(kpi_plots)

