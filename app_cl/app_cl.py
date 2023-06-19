
from flask import Flask, request, jsonify
from time import time, sleep
import logging
from swissknife import process_data_cl, tree_convert_dataframe_to_dict_and_ndarray_to_list_format
from clustering import Clustor
import base64
import pickle

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='cl_service.log', level=logging.INFO)

# initial class
eps = 0.08
min_samples = 30
clustor = Clustor(eps, min_samples)

@app.route('/cluster', methods=['POST'])
def cluster():
    try:
        data = request.get_json(force=True)
        df_clean, df_cl, ne_list = process_data_cl(data)

        merged_df, xcode_df, label_numpy, anomaly_time_dict = clustor.clustering(df_clean, df_cl, ne_list)
        merged_dict = merged_df.to_dict(orient='records')
        # xcode64 = {k: base64.b64encode(pickle.dumps(v)).decode('utf-8') for k, v in xcode_dict.items()}
        # label64 = {k: base64.b64encode(pickle.dumps(v)).decode('utf-8') for k, v in label_dict.items()}
        xcode_dict = tree_convert_dataframe_to_dict_and_ndarray_to_list_format(xcode_df)
        label_dict = tree_convert_dataframe_to_dict_and_ndarray_to_list_format(label_numpy)

        result = {
        'anomaly': merged_dict,
        'xcode': xcode_dict,
        'label': label_dict,
        'anomaly_time': anomaly_time_dict
        }
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 400
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, threaded=True)
