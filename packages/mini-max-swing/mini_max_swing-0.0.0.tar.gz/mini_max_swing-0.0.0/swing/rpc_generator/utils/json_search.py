"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 14:49
@Author: xingyun
"""
import re
import traceback
from rpc_generator.plugins.log.logger import logger


class JsonSearch:
    def __init__(self, resp):
        if isinstance(resp, dict):
            self._json = resp
        else:
            self._json = self.thrift_2_json(resp)
        self.result_list = []

    def thrift_2_json(self, thrift_obj):
        '''
        把rpc请求的response转化成json,序列化
        :param thrift_obj:
        :return:
        '''
        json_data = {}
        # 先判断是否为list结构
        if isinstance(thrift_obj, list):
            type_list = []
            for item in thrift_obj:
                # 如果是list类型，则循环判断list内的元素类型，普通类型直接赋值
                if isinstance(item, (str, int, float, bool)) or (item is None):
                    type_list.append(item)
                else:
                    # 非普通类型，这里又要做一层递归调用
                    ret = self.thrift_2_json(item)
                    type_list.append(ret)
            json_data = type_list
        # 循环遍历thrift对象的字典结构
        else:
            try:
                if isinstance(thrift_obj, tuple):
                    json_data["error_resp"] = thrift_obj
                else:
                    for key, value in thrift_obj.__dict__.items():
                        # 如果是普通类型，则直接赋值
                        if isinstance(value, (str, int, float, bool)) or (value is None):
                            json_data[key] = value
                        elif isinstance(value, list):
                            type_list = []
                            for item in value:
                                # 如果是list类型，则循环判断list内的元素类型，普通类型直接赋值
                                if isinstance(item, (str, int, float, bool)) or (item is None):
                                    type_list.append(item)
                                # elif isinstance(item, list):
                                #     type_list.append(item)
                                else:
                                    # 非普通类型，这里又要做一层递归调用
                                    ret = self.thrift_2_json(item)
                                    type_list.append(ret)
                            json_data[key] = type_list
                        elif isinstance(value, dict):
                            type_dict = {}
                            for k, v in value.items():
                                # 如果是字典类型,需要对字典的value做下判断，普通类型直接赋值
                                if isinstance(v, (str, int, float, bool)) or (v is None):
                                    type_dict[k] = v
                                elif isinstance(v, list):
                                    # 如果是list类型,需要对list的value做下判断，非普通类型，继续递归
                                    type_list = []
                                    for item in v:
                                        # 如果是list类型，则循环判断list内的元素类型，普通类型直接赋值
                                        if isinstance(item, (str, int, float, bool)) or (item is None):
                                            type_list.append(item)
                                        else:
                                            # 非普通类型，这里又要做一层递归调用
                                            ret = self.thrift_2_json(item)
                                            type_list.append(ret)
                                    type_dict[k] = type_list
                                else:
                                    ret = self.thrift_2_json(v)
                                    type_dict[k] = ret
                            json_data[key] = type_dict

                        elif isinstance(value, bytes):
                            json_data[key] = value
                        else:
                            ret = self.thrift_2_json(value)
                            json_data[key] = ret
            except Exception as e:
                logger.info(e)
        return json_data

    def search_key(self, key, index=None):
        '''
        在json中递归查找键值
        :param key:
        :param index:
        :return:
        '''
        self.result_list = []
        try:
            if '.' in key:
                self._search_link(self._json, key)
            else:
                self._search(self._json, key)
            if not index:
                return self.result_list
            else:
                return self.result_list[index]
        except:
            logger.info(f"key:{key},index:{index} not fould!, return None")
            logger.error(traceback.format_exc())
            return None

    def search_keys(self, keys):
        '''
        批量查找json的键值
        :param keys:
        :return:
        '''
        ret = {}
        for key in keys:
            value = self.search_key(key)
            ret[key] = value
        return ret

    def _search(self, json_object, key):
        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self._search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self._search(item, key)

    def _search_link(self, json_object, keys):
        '''
        级联查找键值
        :param json_object:
        :param keys:
        :return:
        '''
        key_list = keys.split('.')
        p = re.compile(r'(?<=\[)[^\[\]]*(?=\])', re.S)
        if len(key_list) == 1:
            try:
                if '[' in keys:
                    keys = re.sub(r"\[.*?\]", "", keys)
                    index = re.search(p, key_list[0]).group(0)
                    self.result_list.append(json_object[keys][int(index)])
                else:
                    self.result_list.append(json_object[keys])
            except:
                self.result_list.append(None)
        else:
            try:
                try:
                    # 这里是为了区分key中有没有下标，把下标正则出来
                    index = re.search(p, key_list[0]).group(0)
                    key_list[0] = re.sub(r"\[.*?\]", "", key_list[0])
                except:
                    index = None
                if isinstance(json_object[key_list[0]], dict):
                    self._search_link(json_object[key_list[0]], '.'.join(key_list[1:]))
                elif isinstance(json_object[key_list[0]], list):
                    if index != None:
                        self._search_link(json_object[key_list[0]][int(index)], '.'.join(key_list[1:]))
                    else:
                        for value in json_object[key_list[0]]:
                            self._search_link(value, '.'.join(key_list[1:]))
                else:
                    self.result_list.append(None)
            except:
                logger.info(f"can`t find {keys}, set None")
                self.result_list.append(None)

    @property
    def json(self):
        return self._json
