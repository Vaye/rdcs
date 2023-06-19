
# from do_plotting import DataVisualizer
from flask import Flask, request, jsonify
import pandas as pd
import logging
import base64
import pickle
from swissknife import generate_image_dict, create_all_plots

# Setup logging
logging.basicConfig(filename='plot_service.log', level=logging.INFO)

app = Flask(__name__)

@app.route('/plot', methods=['POST'])
def plot():
    try:
        """Get the plot for ne"""
        data = request.get_json()
        merged_dict = data.get('rawdata')
        xcode_dict = data.get('xcode')  # Populate this with your data from request
        label_dict = data.get('label')  # Populate this with your data from request
        anomaly_time_dict = data.get('anomaly_time')  # Populate this with your data from request

        df_clean = pd.DataFrame.from_records(merged_dict)
        # xcode_dict = {k: pickle.loads(base64.b64decode(v.encode('utf-8'))) for k, v in xcode64.items()}
        # label_dict = {k: pickle.loads(base64.b64decode(v.encode('utf-8'))) for k, v in label64.items()}

        # 将time列转换为datetime类型
        df_clean['time'] = pd.to_datetime(df_clean['time'])
        # 获取除了'neName'和'time'之外的所有列名（即所有的kpi名称）
        kpi_columns = [col for col in df_clean.columns if col not in ['neName', 'time']]
        
        cl_plots = create_all_plots(xcode_dict, label_dict, angle=(30,330))
        kpi_plots = generate_image_dict(df_clean, kpi_columns, anomaly_time_dict)

        result = {
        'cl': cl_plots,
        'kpi': kpi_plots
        }
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, threaded=True)
