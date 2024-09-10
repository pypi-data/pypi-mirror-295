"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 15:31
@Author: xingyun
"""

import json
import logging
import os


class DataTemplate(object):
    _data_string = """
$data_name = {$data}
    """

    _type_value_link = {
        "string": "",
        "int": 0,
        "object": {},
        "float": 0.0,
        "array": [],
        "bool": True,
        "double": 0.00,
        "bytes": ""
    }

    def generate_template(self, psm, api_info, data_dest_directory=None, version="latest"):
        """
        生成模板方法
        :param data_dest_directory: 生成数据模板的路径
        :param psm: psm名称
        :param api_info: Tesla返回的接口信息
        :param version: 用户传递的版本信息
        :return:
        """
        if not data_dest_directory:
            data_dest_directory = "data/json"
        else:
            data_dest_directory = f"data/json/{data_dest_directory}"

        data_path, content = self.create_data_json_file(psm, data_dest_directory)
        # print("c :", data_path)
        if data_path:
            logging.info(f"创建 data 成功, data_path:{data_path}")
        else:
            print("创建数据文件失败!")
            return

        if not content:
            content['psm'] = psm
            content['version'] = version
            content['result'] = []

        for index, api in enumerate(api_info):
            path = api['path'] if "-" not in api['path'] else api['path'].replace('-', '_')
            method = api['method']
            req_schema = api['req_schema']

            if path == "" or method == "":
                continue

            # 如果存在路径参数加入req_schema
            import re
            path_params = [param[0] for param in re.findall(r':(.*?)(/|$)', path)]
            if path_params:
                req_schema.update({'path_param': {param: f':{param}' for param in path_params}})

            # 这里做替换是防止生成的method_name中带有/，因此全部替换成_
            path = path.replace("/", "_").replace(":", "")
            if path.startswith("_"):
                path = path[1:]
            if path.endswith("_"):
                path = path[:-1]

            if len(content['result']):
                if any(path == result_['name'] for result_ in content['result']):
                    continue
                else:
                    content['result'].append(
                        {"name": path, "request_json": self._generate_data_template(req_schema),
                         "headers_value": {"headers": {"Content-Type": "application/json"}}})
            else:
                content['result'].append(
                    {"name": path, "request_json": self._generate_data_template(req_schema),
                     "headers_value": {"headers": {"Content-Type": "application/json"}}})
        with open(data_path, "w") as fp:
            fp.write(json.dumps(content, indent=4))
        # logging.info(f"gen data file {data_path} successful")
        return data_path

    def _generate_data_template(self, req_schema):
        """
        生成数据模板，为内部调用方法
        :param req_schema: uri path, eg: api/v1/sell/refund_for_qa
        :param req_schema: 接口中返回的req_schema
        :return: 模板内容content -> str
        """

        value = {'body_param': {}, 'query_param': {}, 'files': {}, 'form_data': {}}
        if req_schema:
            if req_schema.get('body_param', None):
                param = req_schema.get('body_param', None)
                value['body_param'] = DataTemplate.parse_body_param({}, param)
            if req_schema.get('form_data', None):
                param = req_schema.get('query_param', None)
                value['form_data'] = DataTemplate.parse_body_param({}, param)

            if req_schema.get('query_param', None):
                param = req_schema.get('query_param', None)
                value['query_param'] = DataTemplate.parse_body_param({}, param)
            if req_schema.get('path_param', None):
                value['path_param'] = req_schema.get('path_param', {})

        return value
        # return DataTemplate.parse_body_param({}, param)

    @staticmethod
    def create_data_json_file(psm, data_dest_directory):
        """
        根据psm名称创建目录文件
        :param psm：psm名称
        :param data_dest_directory: 生成数据模板的目标绝对路径
        :return: 创建成功之后的*.py文件的绝对路径
        """
        psm_str = psm.replace(".", "_")
        data_file_name = f"{psm_str}_data.json"
        # 如果当前文件夹下对应path中提取的文件夹名称不存在，则创建该文件夹，并创建一个__init__.py文件
        if data_dest_directory.startswith("/"):
            data_dest_directory = data_dest_directory[1:]
        if data_dest_directory.endswith("/"):
            data_dest_directory = data_dest_directory[:-1]
        file_path = os.path.join(os.getcwd(), data_dest_directory)

        if "/" in data_dest_directory:
            dir_list = data_dest_directory.split("/")
            path = os.getcwd()
            for dir_ in dir_list:
                path = os.path.join(path, dir_)
                if not os.path.exists(path):
                    os.makedirs(path)
                    open(path + "/__init__.py", "w")
                else:
                    if os.path.exists(path):
                        if not os.path.exists(path + "/__init__.py"):
                            open(path + "/__init__.py", "w")
        else:
            path = os.path.join(os.getcwd(), data_dest_directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(path + "/__init__.py", "w")
            else:
                if not os.path.exists(path + "/__init__.py"):
                    open(path + "/__init__.py", "w")

        # 如果*.json文件不存在的话，创建这个文件
        if not os.path.isfile(os.path.join(file_path, data_file_name)):
            f = open(os.path.join(file_path, data_file_name), "w", encoding='utf8')
            content = {}
        else:
            f = open(os.path.join(file_path, data_file_name), "r", encoding='utf8')
            content = json.loads(f.read())
        return os.path.join(file_path, data_file_name), content

    @staticmethod
    def parse_body_param(struct, body_params):
        """
        解析嵌套json结构体
        :param struct: 初始化传入空{}
        :param body_params: json结构体
        :return:
        """
        if body_params:
            for key, value in body_params.items():
                children = value.get("children", None)
                _type = value.get("type", None)
                optional = value.get("optional", False)

                # 判断为可选项
                if optional:
                    if isinstance(struct, dict):
                        struct[key] = None
                        # struct[key] = body_params[key]['example'] if body_params[key]['example'] != '' else None
                    elif isinstance(struct, list):
                        struct[key] = None
                        # struct = body_params[key]['example'] if body_params[key]['example'] != '' else None
                else:
                    if _type == "int" or _type == "float" or _type == "string" or _type == "double" or _type == "bool" or _type == "bytes":
                        if isinstance(struct, dict):
                            struct[key] = DataTemplate._type_value_link[_type]
                        elif isinstance(struct, list):
                            struct.append(DataTemplate._type_value_link[_type])
                    elif _type == "array":
                        if isinstance(struct, list):
                            struct.append(DataTemplate.parse_body_param(struct=[], body_params=children))
                        elif isinstance(struct, dict):
                            struct[key] = DataTemplate.parse_body_param(struct=[], body_params=children)
                    elif _type == "object":
                        if not children:
                            if isinstance(struct, dict):
                                struct[key] = DataTemplate._type_value_link[_type]
                            elif isinstance(struct, list):
                                struct.append(DataTemplate._type_value_link[_type])
                        else:
                            if isinstance(struct, dict):
                                struct[key] = DataTemplate.parse_body_param(struct={}, body_params=children)
                            elif isinstance(struct, list):
                                struct.append(DataTemplate.parse_body_param(struct={}, body_params=children))
        return struct
