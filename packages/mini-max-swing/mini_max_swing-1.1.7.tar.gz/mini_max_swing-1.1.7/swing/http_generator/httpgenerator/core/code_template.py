"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 15:31
@Author: xingyun
"""
import logging
import os
import re
from string import Template


class CodeTemplate(object):
    _service_string = """import os
import sys

from rpc_generator.utils.utils import Utils
from http_generator.httpclient.core import HTTPClient
from http_generator.httpgenerator.utils.json_parse import JsonParse
from rpc_generator.utils.utils import Utils


# version = $version

class $service_name(object):    
    """
    _decorator_string = """ @xray_trace(psm="$psm", path="$path")"""
    _method_get_string = """
    def $method_name(self, cluster="", refresh_data=None):
        \"\"\"
        refresh_data: 结构体中需要更新的数据, dict类型
        \"\"\"
        file_name = os.path.basename(__file__)          # 获取当前py文件名称
        method_name = sys._getframe().f_code.co_name    # 获取当前func名称
        env = Utils.get_env()
        psm = file_name.replace(".py", "")
        domain = Utils.get_domain(psm, cluster, env)
        data, headers = JsonParse().get_req_json(file_name, method_name, refresh=refresh_data) # 获取更新后的请求数据
        body_param = data.get("body_param", None)
        query_param = data.get("query_param", None)
        url = domain + \"$path\"$path_param_format
        hc = HTTPClient()
        return hc.get(url=url, params=query_param, json_data=body_param, headers=headers)
    """

    _method_post_string = """
    def $method_name(self, cluster="", form_data=None, refresh_data=None):
        \"\"\"
        form_data: 表单数据
        refresh_data: 结构体中需要更新的数据, dict类型
        \"\"\"
        file_name = os.path.basename(__file__)          # 获取当前py文件名称
        method_name = sys._getframe().f_code.co_name    # 获取当前func名称
        
        env = Utils.get_env()
        psm = file_name.replace(".py", "")
        domain = Utils.get_domain(psm, cluster, env)

        data, headers = JsonParse().get_req_json(file_name, method_name, refresh=refresh_data) # 获取更新后的请求结构体
        body_param = data.get("body_param", None)
        query_param = data.get("query_param", None)
        files = data.get("files", None)
        form_data = data.get("form_data", None)
        
        url = domain + \"$path\"$path_param_format
        hc = HTTPClient()
        return hc.post(url=url, form_data=form_data, json_data=body_param, params=query_param, files=files, headers=headers)
    """

    _method_put_string = """
    def $method_name(self, cluster="", form_data=None, refresh_data=None):
        \"\"\"
        form_data: 表单数据
        refresh_data: 结构体中需要更新的数据, dict类型
        \"\"\"
        file_name = os.path.basename(__file__)          # 获取当前py文件名称
        method_name = sys._getframe().f_code.co_name    # 获取当前func名称
        
        env = Utils.get_env()
        psm = file_name.replace(".py", "")
        domain = Utils.get_domain(psm, cluster, env)

        data, headers = JsonParse().get_req_json(file_name, method_name, refresh=refresh_data) # 获取更新后的请求结构体
        body_param = data.get("body_param", None)
        query_param = data.get("query_param", None)
        form_data = data.get("form_data", None)

        url = domain + \"$path\"$path_param_format
        hc = HTTPClient()
        return hc.put(url=url, form_data=form_data, json_data=body_param, params=query_param, headers=headers)
    """

    _method_del_string = """
    def $method_name(self, cluster="", refresh_data=None):
        \"\"\"
        refresh_data: 结构体中需要更新的数据, dict类型
        \"\"\"
        file_name = os.path.basename(__file__)          # 获取当前py文件名称
        method_name = sys._getframe().f_code.co_name    # 获取当前func名称
        
        env = Utils.get_env()
        psm = file_name.replace(".py", "")
        domain = Utils.get_domain(psm, cluster, env)

        data, headers = JsonParse().get_req_json(file_name, method_name, refresh=refresh_data) # 获取更新后的请求结构体
        query_param = data.get("query_param", None)
        files = data.get("files", None)
        
        url = domain + \"$path\"$path_param_format
        hc = HTTPClient()
        return hc.delete(url=url, params=query_param, files=files, headers=headers)
    """

    _method_patch_string = """
    def $method_name(self, cluster='', refresh_data=None):
        \"\"\"
        refresh_data: 结构体中需要更新的数据, dict类型
        \"\"\"
        file_name = os.path.basename(__file__)          # 获取当前py文件名称
        method_name = sys._getframe().f_code.co_name    # 获取当前func名称

        env = Utils.get_env()
        psm = file_name.replace(".py", "")
        domain = Utils.get_domain(psm, cluster, env)

        params, headers = JsonParse().get_req_json(file_name, method_name, refresh=refresh_data) # 获取更新后的请求结构体

        url = domain + \"$path\"$path_param_format
        hc = HTTPClient()
        return hc.patch(url=url, params=params, headers=headers)
    """

    _method_link = {
        "POST": _method_post_string,
        "GET": _method_get_string,
        "PUT": _method_put_string,
        "DELETE": _method_del_string,
        "PATCH": _method_patch_string
    }

    def __init__(self):
        pass

    def generate_template(self, psm, api_info, xray, code_dest_directory=None, version="latest"):
        """
        生成模板方法
        :param psm: psm名称
        :param api_info: Tesla返回的接口信息
        :param code_dest_directory: 生成代码模板的路径
        :param version: 用户传递的版本信息
        :param xray: 启用xray
        :return:
        """
        if not code_dest_directory:
            code_dest_directory = "api"
        else:
            code_dest_directory = f"api/{code_dest_directory}"
        code_path, func_list = self.create_code_py_file(psm, code_dest_directory)
        # logging.info(f"code_dest_directory: {code_path}")
        if code_path:
            logging.info("创建模板文件成功!")
        else:
            logging.warning("创建模板文件失败!")
            return

        psm_str = ''.join(word.capitalize() for word in psm.split('_'))
        content = ""
        step = 0
        for index, api in enumerate(api_info):
            method = api['method']
            path = api['path']
            # print(path)

            if path == "" or method == "":
                continue

            if step == 0 and len(func_list) == 0:
                step += 1
                service_tmp_string = Template(CodeTemplate._service_string)
                content += service_tmp_string.substitute({"service_name": psm_str, "version": version})
                content += self._generate_code_template(psm, method, path, func_list, xray)
            else:
                step += 1
                content += self._generate_code_template(psm, method, path, func_list, xray)

        with open(code_path, 'a+') as f:
            f.write(content)
        logging.info(f"创建 api 成功，api_path： {code_path}")
        return code_path

    def _generate_code_template(self, psm, method, path, func_list, xray):
        """
        生成代码模板，仅为内部调用
        :param method: 方法名称
        :param path: 接口uri path, eg:api/v1/sell/refund_for_qa
        :param req_schema: Tesla接口中返回的req_schema
        :param resp_schema: Tesla接口中返回的resp_schema
        :return: 模板内容content -> str
        """

        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        method_name = path.replace("/", "_").replace(":", "").replace("-", "_")

        # 处理路径参数作为变量从 data['path_param'] 下的字典取值
        path_params = [param[0] for param in re.findall(r':(.*?)(/|$)', path)]
        for param in path_params:
            path = path.replace(f':{param}', f'{{{param}}}')

        template_str = CodeTemplate._method_link[method]

        if xray:
            template_str = CodeTemplate._decorator_string + CodeTemplate._method_link[method]
        # 创建template实例
        method_tmp_string = Template(template_str)
        # print(f"method name ======{method_name}")
        if method_name in func_list:  # 防止重复方法名的添加
            content = ""
            sub_dict = {"method_name": method_name, "path": "/" + path, "psm": psm,
                        'path_param_format': ".format(**data.get('path_param'))" if path_params else ''}
            # print(sub_dict)
        else:
            sub_dict = {"method_name": method_name, "path": "/" + path, "psm": psm,
                        'path_param_format': ".format(**data.get('path_param'))" if path_params else ''}
            # print(sub_dict)
            content = method_tmp_string.substitute(sub_dict)
        return content

    @staticmethod
    def create_code_py_file(psm, code_dest_directory):
        """
        根据psm名称创建目录文件
        :param psm：psm名称
        :param code_dest_directory: 生成代码模板的目标绝对路径，在该目录下创建业务的API层代码
        :return: 创建成功之后的*.py文件的绝对路径
        """
        psm_str = psm.replace(".", "_")
        template_file_name = f"{psm_str}.py"

        # file_path = os.path.join(os.getcwd(), code_dest_directory)
        # 如果当前文件夹下对应path中提取的文件夹名称不存在，则创建该文件夹，并创建一个__init__.py文件
        if code_dest_directory.startswith("/"):
            code_dest_directory = code_dest_directory[1:]
        if code_dest_directory.endswith("/"):
            code_dest_directory = code_dest_directory[:-1]
        file_path = os.path.join(os.getcwd(), code_dest_directory)

        if "/" in code_dest_directory:
            dir_list = code_dest_directory.split("/")
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
            path = os.path.join(os.getcwd(), code_dest_directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(path + "/__init__.py", "w")
            else:
                if not os.path.exists(path + "/__init__.py"):
                    open(path + "/__init__.py", "w")

        # 如果*.py文件不存在的话，创建这个文件
        code_file_path = os.path.join(file_path, template_file_name)
        if not os.path.isfile(code_file_path):
            f = open(code_file_path, "w", encoding='utf8')
            func_list = []
        else:
            f = open(code_file_path, "r", encoding='utf8')
            func_list = re.findall(r"def\s*(.*)[(]self", f.read())
            # print(func_list)

        return code_file_path, func_list
