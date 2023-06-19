
from flask import Flask, request, jsonify
import numpy as np
import joblib
import torch
from time import time, sleep
import logging
from do_reduction import Reducer

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
reducer = Reducer('models/tj_amf_state_model.pth', device)

@app.route('/dimreduction', methods=['POST'])
def dimreduction():
    try:
        data = request.get_json(force=True)
        ds = np.array(data["ds_norm"])
        # 对数据进行归一化
        scaler = joblib.load('models/scaler.save')
        ds_norm=scaler.transform(ds).tolist()
        xcode = reducer.reduction(ds_norm)
        result = {'xcode':xcode} #list
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 400
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
