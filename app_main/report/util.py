#!/usr/bin/env python3
# encoding: utf-8
import base64
import json
import hashlib
from report import config


def hash_md5_content(content):
    content_str = str(content)
    m = hashlib.md5()
    m.update(content_str.encode())
    return m.hexdigest()


def hash_md5_file(file_obj):
    return hashlib.md5(file_obj).hexdigest()


def parse_request_id(gateway_param):
    return parse_gateway_param(gateway_param)['ability_invoking_request_id']


def parse_gateway_param(gateway_param):
    if gateway_param is None or gateway_param == '':
        gateway_param = config.MOCK_APP_PARAM
    return eval(gateway_param)


def generate_header(gateway_param):
    app_dict = parse_gateway_param(gateway_param)
    app_dict[config.PARAM_SDK_VER] = config.SDK_VERSION
    base64_param = base64.b64encode(bytes(json.dumps(app_dict), config.STR_CHARACTER)).decode()
    return base64_param + '.sdk'

