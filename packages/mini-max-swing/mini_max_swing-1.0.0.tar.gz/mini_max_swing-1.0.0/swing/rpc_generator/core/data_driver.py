"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:52
@Author: xingyun
"""
import os
import re
import json
import traceback
from rpc_generator.plugins.log.logger import logger


class JsonUpdate:
    @staticmethod
    def update_keys(json_a, json_b, idl_path=None):
        """
        批量更新json的key
        :param json_a: 要更新的目标JSON对象
        :param json_b: 包含新键值对的源JSON对象
        :param idl_path: idl的地址 用于判断key是不是required
        :return: 更新后的JSON对象
        """
        try:
            for key, value in json_b.items():
                if key == "__type":
                    # 如果jsonA中没有该键，或者该键的值为空，则添加或更新
                    if key not in json_a or not json_a[key]:
                        json_a[key] = value
                elif JsonUpdate.is_key_required(key=key, idl_path=idl_path) and key not in json_a:
                    json_a[key] = value

                elif isinstance(value, dict):
                    # 如果值是字典，递归调用merge_json_types
                    if key in json_a and isinstance(json_a[key], dict):
                        JsonUpdate.update_keys(json_a[key], value, idl_path=idl_path)
                elif isinstance(value, list):
                    # 如果值是列表，遍历列表并更新每个元素
                    if key in json_a and isinstance(json_a[key], list):
                        for i, item in enumerate(value):
                            if isinstance(item, dict):
                                JsonUpdate.update_keys(json_a[key][i], item, idl_path=idl_path)
                            elif isinstance(item, list):
                                JsonUpdate.update_keys(json_a[key][i], item, idl_path=idl_path)
                            else:
                                # 如果列表中的元素不是字典也不是列表，直接更新
                                json_a[key][i] = item
        except Exception as e:
            logger.warning(f"update keys error, for {e}")
            return

    def update_link_key(self, key_update, value_update, json_data):
        """
        更新级联的key,比如a.b.c，遇到list也可以继续往下查询
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
            if isinstance(json_data[key_list[0]], dict):
                # 如果是字典类型，则继续递归
                self.update_link_key('.'.join(key_list[1:]), value_update, json_data[key_list[0]], )
            elif isinstance(json_data[key_list[0]], list):
                if index != None:
                    # 如果是list，看下有没有index下标，如果有下标，取出指定下标的值，然后递归
                    self.update_link_key('.'.join(key_list[1:]), value_update, json_data[key_list[0]][int(index)])
                else:
                    # 如果没有下标，则循环递归
                    for value in json_data[key_list[0]]:
                        self.update_link_key('.'.join(key_list[1:]), value_update, value)

    def _search(self, key_search, json_data):
        """
        递归查询json中的某个key值
        :param key_search:
        :param json_data:
        :return:
        """
        for k, v in json_data.items():
            if k == key_search:
                return v
            if isinstance(v, dict):
                return self._search(key_search, v)
            if isinstance(v, list):
                for v_in_list in v:
                    if isinstance(v_in_list, dict):
                        return self._search(key_search, v_in_list)

    @staticmethod
    def is_key_required(idl_path, key):
        """
        判断key是不是个必传参数
        :param idl_path:
        :param key:
        :return:
        """
        # 读取 IDL 文件内容
        # print(f'====The idl_path is {idl_path}， The key is :{key}')
        with open(idl_path, 'r') as file:
            idl_content = file.read()

        # 解析 include 的文件
        include_pattern = re.compile(r'^include\s+"([^"]+)"', re.MULTILINE)
        includes = include_pattern.findall(idl_content)

        # 读取 include 的文件内容
        for include_file in includes:
            include_path = os.path.join(os.path.dirname(idl_path), include_file)
            with open(include_path, 'r') as file:
                idl_content += '\n' + file.read()

        # 正则表达式匹配结构体中的字段
        # field_pattern = re.compile(r'\b(required|optional)\b\s+(\w+\.)?\b' + re.escape(key) + r'\b')
        field_pattern = re.compile(r'\d+:\s+(required|optional)\s+[^\s]+\s+' + re.escape(key) + r'\b')

        # 查找是否有 required 的 key
        match = field_pattern.search(idl_content)
        if match and match.group(1) == 'required':
            return True
        return False


class JsonSearch:
    def __init__(self, resp):
        if isinstance(resp, dict):
            self._json = resp
        else:
            self._json = self.thrift_2_json(resp)
        self.result_list = []

    def thrift_2_json(self, thrift_obj):
        """
        把rpc请求的response转化成json,序列化
        :param thrift_obj:
        :return:
        """
        json_data = {}
        # 循环遍历thrift对象的字典结构
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
                    else:
                        # 如果是字典类型,需要对字典的value做下判断，非普通类型，继续递归
                        ret = self.thrift_2_json(v)
                        type_dict[k] = ret
                json_data[key] = type_dict
            else:
                ret = self.thrift_2_json(value)
                json_data[key] = ret
        return json_data

    def search_key(self, key, index=None):
        """
        在json中递归查找键值
        :param key:
        :param index:
        :return:
        """
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
        """
        批量查找json的键值
        :param keys:
        :return:
        """
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
        """
        级联查找键值
        :param json_object:
        :param keys:
        :return:
        """
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


if __name__ == "__main__":
    test_data = {"Items": [{"Points": [{
        "X": 0.14706489443778992,
        "Y": 0.029663970693945885
    }], "SimilarItems": [{"ItemId": "1111"}, {"ItemId": "2222"}]}]}
    get_value = JsonSearch(test_data)
    print(json.dumps(get_value.search_keys(['Items[0].SimilarItems[1]'])))
