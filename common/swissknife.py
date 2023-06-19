import pandas as pd
import joblib
import json
import io
import base64
import matplotlib
matplotlib.use('Agg')  # 在其他任何matplotlib导入之前设置
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from PIL import Image

# def preprocess_data(data):
#     df_drop = data.dropna() # 去掉丢失数据的样本
#     df_drop = df_drop.drop_duplicates()
#     df_clean = df_drop.reset_index(drop=True)

#     # 提取网元名称和时间戳
#     ne_time_column_list = ['neName','time'] 
#     kpi_list = [c for c in df_clean.columns.tolist() if c not in ne_time_column_list] # KPI表头

#     df_ne_time = df_clean[ne_time_column_list] # 网元名称和时间

#     ds = df_clean[kpi_list].to_numpy()

#     # 对数据进行归一化
#     scaler = joblib.load('models/scaler.save')
#     ds_norm=scaler.transform(ds).tolist()

#     return df_clean, df_ne_time, ds_norm

def preprocess_data(data):
    df_drop = data.dropna() # 去掉丢失数据的样本
    df_drop = df_drop.drop_duplicates()
    df_clean = df_drop.reset_index(drop=True)

    # 提取网元名称和时间戳
    ne_time_column_list = ['neName','time'] 
    kpi_list = [c for c in df_clean.columns.tolist() if c not in ne_time_column_list] # KPI表头

    df_ne_time = df_clean[ne_time_column_list] # 网元名称和时间

    ds = df_clean[kpi_list].to_numpy()

    # # 对数据进行归一化
    # scaler = joblib.load('models/scaler.save')
    # ds_norm=scaler.transform(ds).tolist()

    return df_clean, df_ne_time, ds

def process_data_cl(data):
    df_clean = pd.DataFrame(data['rawdata'])
    xcode = data['xcode']
    ne_time = pd.DataFrame(data['ne_time']).to_numpy().tolist()

    list0 = [a+b for a, b in zip(ne_time, xcode)]
    df_cl = pd.DataFrame(list0, columns=['ne','time','x0','x1','x2'])
    ne_list = list(set(df_cl['ne']))
    
    return df_clean, df_cl, ne_list


def print_list_structure(lst, level=0):
    print('  ' * level + str(type(lst)))
    if isinstance(lst, list):
        for item in lst:
            if isinstance(item, list):
                print_list_structure(item, level + 1)

def clustering(data, eps=0.1, min_samples=30):  
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    labels = db.labels_
    
    return labels

def generate_image_dict(df_clean, kpi_columns, anomaly_time_dict):
    result_dict = {}

    for ne in df_clean['neName'].unique():
        df_ne = df_clean[df_clean['neName'] == ne]
        
        ne_dict = {}
        for kpi in kpi_columns:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df_ne['time'], df_ne[kpi])
            if ne in anomaly_time_dict:
                for anomaly_time in anomaly_time_dict[ne]:
                    anomaly_time = pd.to_datetime(anomaly_time)
                    anomaly_value = df_ne.loc[df_ne['time'] == anomaly_time, kpi]
                    ax.plot(anomaly_time, anomaly_value, 'ro')

            # 将图像保存为PNG格式的二进制数据
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)

            # 将二进制数据编码为Base64字符串
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')

            ne_dict[kpi] = image_base64

        result_dict[ne] = ne_dict
    
    return result_dict


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



def plot_result_3d(data, labels, neName, angle=(30,30)):
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    
    fig = plt.figure(figsize=(20, 20))
    ax = plt.subplot(111, projection='3d')
    
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 1, 1]
            m='x'
        else:
            m='.'
    
        class_member_mask = (labels == k)
        
        xy = data[class_member_mask]
        ax.scatter(xy[:,0], xy[:,1], xy[:,2], c=col,marker=m)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(*angle)

    # Adding title to the plot
    ax.set_title(neName)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)  # Close the figure

    # Create a dictionary with the plot data
    plot_dict = {neName: base64.b64encode(buf.getvalue()).decode('utf-8')}
    
    return plot_dict

def create_all_plots(xcode_dict, label_dict, angle=(30,330)):
    all_plots = {}
    
    for ne, df_dict in xcode_dict.items():
        xcode_df = pd.DataFrame(df_dict)
        data = xcode_df[['x0','x1','x2']].values
        labels = np.array(label_dict[ne])
        
        plot_dict = plot_result_3d(data, labels, neName=ne, angle=angle)
        
        all_plots.update(plot_dict)
    
    return all_plots


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


def tree_convert_dataframe_to_dict_and_ndarray_to_list_format(node):
    if isinstance(node, pd.DataFrame):
        return node.to_dict()
    elif isinstance(node, np.ndarray):
        return node.tolist()
    elif isinstance(node, list):
        return [tree_convert_dataframe_to_dict_and_ndarray_to_list_format(v) for v in node]
    elif isinstance(node, dict):
        return {k: tree_convert_dataframe_to_dict_and_ndarray_to_list_format(v) for k, v in node.items()}
    else:
        return node