"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:51
@Author: xingyun
"""

import os
import sys
from rpc_generator.utils.utils import Utils
from rpc_generator.core.data_driver import JsonUpdate


class BaseService(object):
    def __init__(self, client_path, data_path):
        self.client_path = client_path
        self.data_path = data_path

    def get_req_json(self, method_name, refresh=None, base=None):
        if refresh is None:
            refresh = {}
        if base is not None:
            refresh['Base'] = base

        json_path = self.get_json_path(self.psm)
        json_data = Utils.get_json_data(json_path)
        methods = json_data["result"][0]["method"]
        for method in methods:
            if method["name"] == method_name:
                if refresh:
                    JsonUpdate().update_keys(refresh, method["request_json"], idl_path=self.rpc_driver.idl_path)
                return refresh
        raise ValueError(f"can`t find {method_name} from json file, please check!")

    def get_dirname(self, file_path):
        path_list = file_path.split(os.sep)
        # index = path_list.index("modules")
        return path_list[-2]

    def get_json_path(self, psm):
        file_name = '_'.join(psm.split('.'))
        root = os.path.dirname(os.path.dirname(os.path.dirname(self.client_path)))
        json_dir = os.path.join(root, self.data_path, "json", self.business)
        if not os.path.exists(json_dir):
            abs_path = os.path.abspath(sys.argv[0])
            root = os.path.dirname(os.path.dirname(os.path.dirname(abs_path)))
            json_dir = os.path.join(root, self.data_path, "json", self.business)
        for root, dirs, files in os.walk(json_dir):
            psm_json = ''
            for file in files:
                if file == f"{file_name}_{self.service}.json":
                    return os.path.join(root, file)
                elif file == f"{file_name}.json":
                    psm_json = file
            if psm_json != '':
                return os.path.join(root, psm_json)

        raise FileNotFoundError(f"{file_name}.json not found!")
