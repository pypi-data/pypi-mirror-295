"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/25 15:31
@Author: xingyun
"""

import json
import os
import re
from swing.rpc_generator.utils.utils import Utils


class JsonParse(object):
    @staticmethod
    def get_json_path(file_name):
        """
        框架中底层所使用的方法，业务不建议使用，用于获取指定文件所在的目录
        :param file_name: 文件名称
        :return: 文件路径
        """
        file_name = 'test_' + file_name.replace(".py", "") + "_data"
        json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "json")
        for root, dirs, files in os.walk(json_dir):
            for file in files:
                if file == f"{file_name}.json":
                    return os.path.join(root, file)
        raise FileNotFoundError(f"{file_name}.json not found!")

    @staticmethod
    def get_json_data(path):
        """
        框架中底层所使用的方法，业务可以使用，获取json文件中的json内容
        :param path: 文件路径
        :return: 文件内容
        """
        with open(path, 'r') as f:
            load_dict = json.load(f)
        return load_dict

    def get_req_json(self, file_name, method_name, refresh=None):
        """
        框架中底层所使用的方法，业务一般不建议使用，用于更新json结构体中的key/value值
        :param file_name: 文件名称
        :param method_name: 方法名称
        :param refresh: 需要更新的数据
        :return:
        """
        if refresh is None:
            refresh = {}
        json_path = self.get_json_path(file_name)
        json_data = self.get_json_data(json_path)
        methods = json_data["result"]
        for method in methods:
            if method["name"] == method_name:
                if refresh:
                    if Utils.get_env_label():
                        self.update_keys(refresh, method['request_json'])
                        self.update_keys(refresh, method['headers_value'])
                        method['headers_value']['headers']['x-tt-env'] = Utils.get_env_label()
                    else:
                        self.update_keys(refresh, method['request_json'])
                        self.update_keys(refresh, method['headers_value'])
                return method['request_json'], method['headers_value']['headers']
        raise ValueError(f"can`t find {method_name} from json file, please check!")

    def update_keys(self, update, json_data):
        """
        框架中底层所使用的方法，业务一般不建议使用，批量更新json的key
        :param update:
        :param json_data:
        :return:
        """
        for key, value in update.items():
            if '.' in key:
                # 如果key中带.,说明是级联形式，如a.b.c，走级联更新逻辑
                self.update_link_key(key, value, json_data)
            else:
                # 普通key值，单一key，直接递归查找
                self.update_key(key, value, json_data)

    def update_link_key(self, key_update, value_update, json_data):
        """
        框架中底层所使用的方法，业务一般不建议使用，更新级联的key,比如a.b.c，遇到list也可以继续往下查询
        :param key_update:
        :param value_update:
        :param json_data:
        :return:
        """
        key_list = key_update.split('.')
        # 递归结束条件，如果已经到了最后一层，直接更新
        if len(key_list) == 1:
            if key_list[0] in json_data.keys():
                json_data[key_list[0]] = value_update
            else:
                raise KeyError(f"can`t find {key_list[0]}")
        else:
            try:
                # 这里是判断输入的key有没有index下标，如a[0].b.c这种，将下标正则出来
                p = re.compile(r'(?<=\[)[^\[\]]*(?=\])', re.S)
                index = re.search(p, key_list[0]).group(0)
                key_list[0] = re.sub(r"\[.*?\]", "", key_list[0])
            except:
                index = None
            if json_data.get(key_list[0], None):
                if isinstance(json_data[key_list[0]], dict):
                    # 如果是字典类型，则继续递归
                    self.update_link_key('.'.join(key_list[1:]), value_update, json_data[key_list[0]], )
                elif isinstance(json_data[key_list[0]], list):
                    if index is not None:
                        # 如果是list，看下有没有index下标，如果有下标，取出指定下标的值，然后递归
                        self.update_link_key('.'.join(key_list[1:]), value_update, json_data[key_list[0]][int(index)])
                    else:
                        # 如果没有下标，则循环递归
                        for value in json_data[key_list[0]]:
                            self.update_link_key('.'.join(key_list[1:]), value_update, value)
            else:
                return

    def update_key(self, key_update, value_update, json_data):
        """
        框架中底层所使用的方法，业务一般不建议使用，更新json的key值，单个key值，不带级联
        :param key_update:
        :param value_update:
        :param json_data:
        :return:
        """
        for k, v in json_data.items():
            if k == key_update:
                json_data[k] = value_update
                break
            if isinstance(v, dict):
                self.update_key(key_update, value_update, v)
            if isinstance(v, list):
                for v_in_list in v:
                    if isinstance(v_in_list, dict):
                        self.update_key(key_update, value_update, v_in_list)
