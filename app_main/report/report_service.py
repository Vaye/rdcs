# -*- coding: utf-8 -*
from report import util, config, data_service
from report.config import sdk_logger
from report.collector import ReportCollector
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

pool = ThreadPoolExecutor(cpu_count() - 1)


def report(collector: ReportCollector):
    pool.submit(__execute_report, collector)


def __execute_report(collector: ReportCollector):
    # 入参转换，文件上传
    gateway_param = collector.get_header_param()
    if collector.get_print_req_id():
        sdk_logger.info("[sdk]request id=" + util.parse_request_id(gateway_param))
    input_dict = __build_input_dict(collector, gateway_param)
    # 上报参数构造
    request_param = __build_request(collector, input_dict, gateway_param)
    sdk_logger.info("[sdk]request build ok, start report!request: %s", request_param)
    data_service.send_data(collector.get_url(), request_param)


def __build_request(collector: ReportCollector, input_dict, gateway_param):
    request_param = {}
    try:
        input_hash = util.hash_md5_content(input_dict)
        output_hash = util.hash_md5_content(collector.get_output_data())
        input_compressed = False
        output_compressed = False
        input_remote_id = None
        output_remote_id = None
        if len(str(input_dict)) > int(config.COMPRESSED_SIZE):
            input_remote_key = config.PARAM_INPUT + input_hash
            input_remote_id = data_service.upload_file(input_remote_key, str(input_dict), gateway_param)
            input_compressed = True
        if len(str(collector.get_output_data())) > int(config.COMPRESSED_SIZE):
            output_remote_key = config.PARAM_OUTPUT + output_hash
            output_remote_id = data_service.upload_file(
                output_remote_key, str(collector.get_output_data()), gateway_param)
            output_compressed = True

        # 参数组装，调用上报接口
        gateway_dict = util.parse_gateway_param(gateway_param)
        request_param = {
            config.PARAM_REQ_APP: gateway_dict[config.PARAM_REQ_APP],
            config.PARAM_REQ_CALLER: gateway_dict[config.PARAM_REQ_CALLER],
            config.PARAM_REQ_ORG: gateway_dict[config.PARAM_REQ_ORG],
            config.PARAM_REQ_ID: gateway_dict[config.PARAM_REQ_ID_KEY],
            config.PARAM_REQ_TIME: int(collector.get_request_time() * 1000),
            config.PARAM_REQ_URL: collector.get_url(),
            config.PARAM_REQ_META: {
                config.PARAM_REQ_TYPE: collector.get_service_type().value,
                config.PARAM_REQ_CODE: collector.get_response_code(),
                config.PARAM_REQ_COST: int((time.time() - collector.get_request_time()) * 1000),
                config.PARAM_REQ_RESULT: collector.get_biz_result().value
            },
            config.PARAM_REQ_INPUT: input_remote_id if input_compressed else input_dict,
            config.PARAM_REQ_OUTPUT: output_remote_id if output_compressed else collector.get_output_data(),
            config.PARAM_REQ_INPUT_HASH: input_hash,
            config.PARAM_REQ_OUTPUT_HASH: output_hash,
            config.PARAM_REQ_INPUT_COMPRESS: input_compressed,
            config.PARAM_REQ_OUTPUT_COMPRESS: output_compressed
        }
    except Exception as e:
        sdk_logger.error("[sdk]build report request error! url: %s, error: %s", collector.get_url(), repr(e))
    return request_param


def __build_input_dict(collector: ReportCollector, gateway_param):
    input_dict = {}
    try:
        if len(collector.get_json_param()) > 0:
            input_dict = collector.get_json_param()
        if len(collector.get_base_param()) > 0:
            input_dict.update(collector.get_base_param())
        if len(collector.get_file_param()) > 0:
            for key in collector.get_file_param().keys():
                file_origin_name = key
                obj = collector.get_file_param().get(key)
                obj_content = obj.read()
                file_id = data_service.upload_file(file_origin_name, obj_content, gateway_param)
                input_dict[file_origin_name] = file_id
    except Exception as e:
        sdk_logger.error("[sdk]build input error! url: %s, error: %s", collector.get_url(), repr(e))
    return input_dict
