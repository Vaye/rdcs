# -*- coding: utf-8 -*

from report import config
import time
import json


class ReportCollector:

    def __init__(self,
                 url: str,
                 is_async: bool = False):
        self.__request_time = time.time()
        self.__http_url = url
        self.__method_is_async = is_async
        self.__code = config.DEFAULT_CODE
        self.__biz_result = None
        self.__gateway_header_param = ''
        # 接口出入参
        self.__single_param_dict = {}
        self.__multi_param_dict = {}
        self.__file_param_dict = {}
        self.__output_dict = {}
        self.__print_req_id = False


    @staticmethod
    def url(url: str,
            is_async: bool = False):
        return ReportCollector(url, is_async)

    def print_req_id(self, is_print=False):
        self.__print_req_id = is_print
        return self

    def header_param(self, header_param: str):
        self.__gateway_header_param = header_param
        return self

    def response_code(self, response_code: int):
        self.__code = response_code
        return self

    def is_success(self, is_success: bool):
        self.__biz_result = is_success
        return self

    def file_param(self, file_name: str, file_obj):
        self.__file_param_dict[file_name] = file_obj
        return self

    def single_param(self, param_name: str, param_value: str):
        self.__single_param_dict[param_name] = param_value
        return self

    def multi_param(self, multi_param: dict):
        if multi_param is None:
            return self
        self.__multi_param_dict.update(multi_param)
        return self

    def output_data(self, output_data):
        if not isinstance(output_data, dict):
            try:
                self.__output_dict = json.loads(output_data)
            except Exception:
                self.__output_dict = {config.PARAM_RESP: str(output_data)}
        else:
            self.__output_dict = output_data
        return self

    # get方法
    def get_request_time(self):
        return self.__request_time

    def get_output_data(self):
        return self.__output_dict

    def get_url(self):
        return self.__http_url

    def get_service_type(self):
        return config.ServiceType.Async if self.__method_is_async else config.ServiceType.Sync

    def get_response_code(self):
        return self.__code

    def get_biz_result(self):
        if self.__biz_result is None:
            return config.BizResult.Unknown
        elif self.__biz_result:
            return config.BizResult.Succeed
        else:
            return config.BizResult.Failed

    def get_base_param(self):
        return self.__single_param_dict

    def get_json_param(self):
        return self.__multi_param_dict

    def get_file_param(self):
        return self.__file_param_dict

    def get_header_param(self):
        return self.__gateway_header_param

    def get_print_req_id(self):
        return self.__print
