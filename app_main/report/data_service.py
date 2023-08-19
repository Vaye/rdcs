# -*- coding: utf-8 -*
from report import config, util
from report.config import sdk_logger
import requests
import json


def upload_file(file_name, file_data, gateway_param):
    files = {config.PARAM_FILE: (file_name, file_data)}
    params = {}
    if '.' in file_name:
        params = {config.PARAM_EXT: file_name.split('.')[-1]}
    if isinstance(file_data, str):
        params[config.PARAM_HASH] = util.hash_md5_content(file_data)
    else:
        params[config.PARAM_HASH] = util.hash_md5_file(file_data)
    try:
        headers = {config.PARAM_TOKEN: util.generate_header(gateway_param)}
        response = requests.post(url=config.SERVER_UPLOAD_URL, files=files, headers=headers, params=params)
        response_json = response.json()
        if response_json[config.PARAM_STATE] != config.PARAM_OK:
            sdk_logger.error("[sdk]upload file error! response:%s", response_json[config.PARAM_MESSAGE])
            return 'error_id'
        file_url = response.json()[config.PARAM_BODY][config.PARAM_URL]
        sdk_logger.info("[sdk]upload file success!file_name: %s url: %s", file_name, file_url)
        return file_url
    except Exception as e:
        sdk_logger.error("[sdk]upload file error! fileName: %s, error: %s", file_name, repr(e))
        return 'error_id'


def send_data(url, request_param):
    headers = {config.PARAM_CONTENT_TYPE: config.PARAM_CONTENT_TYPE_JSON}
    try:
        response = requests.post(url=config.SERVER_FLUENTD_URL, data=json.dumps(request_param), headers=headers)
        if response.status_code != config.HTTP_SUCCESS_CODE:
            sdk_logger.error("[sdk]send data error! response:%s", response)
            return ''
        sdk_logger.info("[sdk]send data success!url: %s", url)
    except Exception as e:
        sdk_logger.error("[sdk]send data error! url: %s, error: %s", url, repr(e))
