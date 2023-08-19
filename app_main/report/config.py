# !/usr/bin/env python3
# encoding: utf-8

import logging
import os
from enum import Enum


class ServiceType(Enum):
    Sync = "sync"
    Async = 'async'


class BizResult(Enum):
    Unknown = 0
    Succeed = 1
    Failed = 2


def logger_config():
    sdk_handler = logging.StreamHandler()
    sdk_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sdk_handler.setFormatter(formatter)

    logger = logging.getLogger("report_sdk")  # sdk logger
    logger.setLevel(logging.INFO)
    logger.addHandler(sdk_handler)

    logger.propagate = False
    return logger


sdk_logger = logger_config()

FLUENTD_URL = 'http://localhost:39010/wvR35wibPQfdUJsK6qi9Y'
SERVER_FLUENTD_URL = str(os.environ.get('FLUENTD_URL', FLUENTD_URL))

UPLOAD_URL = 'http://data-collection-agent.yysc:39010/api/v1/dc-agent/rpc/file/upload'
SERVER_UPLOAD_URL = str(os.environ.get('UPLOAD_URL', UPLOAD_URL))

SDK_VERSION = 1
MOCK_APP_PARAM = '{"app_id":"app-77vnpvmvo2732p", "caller":"hcy74", "org":"sgs-jiangsu", ' \
                 '"ability_invoking_request_id": "0603fdb82d9aca5c89a705f7b7a83544"} '

DEFAULT_SIZE = 200
COMPRESSED_SIZE = str(os.environ.get('COMPRESSED_SIZE', DEFAULT_SIZE))

REPORT_FILE_DIR = '/home/sdk/report_log'
DEFAULT_CODE = 200
PARAM_RESP = "resp"
PARAM_JSON = "json_param"
PARAM_FILE = "file"
PARAM_EXT = "ext"
PARAM_HASH = "hash"
PARAM_TOKEN = "access_token"
PARAM_STATE = "state"
PARAM_BODY = "body"
PARAM_OK = "OK"
PARAM_URL = "url"
PARAM_MESSAGE = "resultMessage"
PARAM_CONTENT_TYPE = "content-type"
PARAM_CONTENT_TYPE_JSON = "application/json"
PARAM_INPUT = "input_"
PARAM_OUTPUT = "output_"
PARAM_REQ_APP = "app_id"
PARAM_REQ_CALLER = "caller"
PARAM_REQ_ORG = "org"
PARAM_REQ_ID = "req_id"
PARAM_REQ_TIME = "req_time"
PARAM_REQ_URL = "url"
PARAM_REQ_META = "meta"
PARAM_REQ_TYPE = "type"
PARAM_REQ_CODE = "code"
PARAM_REQ_COST = "time_cost"
PARAM_REQ_RESULT = "result"
PARAM_REQ_INPUT = "input"
PARAM_REQ_OUTPUT = "output"
PARAM_REQ_INPUT_HASH = "input_hash"
PARAM_REQ_OUTPUT_HASH = "output_hash"
PARAM_REQ_INPUT_COMPRESS = "input_compressed"
PARAM_REQ_OUTPUT_COMPRESS = "output_compressed"
PARAM_REQ_ID_KEY = "ability_invoking_request_id"
PARAM_REQ_HEADER_NAME = "ability_invoking_param"
PARAM_SDK_VER = 'sdk_ver'
STR_CHARACTER = 'utf-8'
HTTP_SUCCESS_CODE = 200
