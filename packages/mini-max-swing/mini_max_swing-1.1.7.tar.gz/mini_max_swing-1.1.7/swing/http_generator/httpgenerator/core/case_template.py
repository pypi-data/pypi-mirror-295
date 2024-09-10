"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 15:31
@Author: xingyun
"""

import json
import logging
import os.path
import re

from string import Template


class CaseTemplate(object):
    _service_string = '''import pytest
from api.$p_psm import $service_name
from common.common import Common


class Test$method_name_1:
    @pytest.mark.P0
    def test_$method_name(self):
        """
        用例描述：测试$method_name 接口正常情况
        """
        caseparam = {
            "env": "all",
            "api_method": $service_name().$method_name,
            "headers": $header_params,
            "query_param": $query_params,
            "body_param": $body_params,
            "debug": True,
            "expect": {
                "stcAssertPart": {
                    "statusInfo": {
                        "code": 0
                    }
                }
            }
        }
        Common.api_handle(caseparam)
    '''
    _conftest_strings = '''import pytest


@pytest.fixture(scope="module")
def test_print():
    string = "这是fixture的示例"
    return string


@pytest.fixture(scope="session")
def s1():
    pass
    '''

    def __init__(self):
        pass

    def generate_template(self, psm=None, case_dest_directory=None, api_info=None):
        if not case_dest_directory:
            case_dest_directory = f"testcase/{psm}"
        else:
            case_dest_directory = f"testcase/{case_dest_directory}/{psm}"
        abs_case_path = os.path.join(os.getcwd(), case_dest_directory)
        for case_info in api_info:
            case_path, content = self.create_case_py_file(case_dest_directory, case_info=case_info)
            # print("case_dest_directory: ", case_path)
            if content != '':
                logging.info(f"case 存在 跳过, case_dest_directory is :{case_path} ")
                continue
            service_tmp_string = Template(CaseTemplate._service_string)
            parts = case_info['path'].split('/')
            result = []
            for part in parts[1:]:
                result.append(part[0].upper() + part[1:])
            method_name_1 = "".join(result)
            service_name = ''.join(word.capitalize() for word in psm.split('_'))
            header_params = {}
            for key in case_info['header']:
                header_params[key] = case_info['header'][key]['example'] if case_info['header'][key][
                                                                               'example'] != '' else ''
            query_params = {}
            for key in case_info['req_schema']['query_param']:
                query_params[key] = case_info['req_schema']['query_param'][key]['example']
            body_params = {}
            for key in case_info['req_schema']['body_param']:
                body_params[key] = case_info['req_schema']['body_param'][key]['example']
            content += service_tmp_string.substitute(
                {
                    "service_name": service_name, "p_psm": psm, "method_name": case_info['path'].replace('/', '_')[1:],
                    "method_name_1": method_name_1, "header_params": header_params,
                    "query_params": query_params, "body_params": body_params,
                }
            )
            with open(case_path, 'a+') as f:
                f.write(content)
            logging.info(f"创建 case 成功, case_dest_directory is :{case_path} ")

    @staticmethod
    def create_case_py_file(case_dest_directory, case_info=None):
        """
        创建demo目录
        :param case_dest_directory: 生成用例模板的目标绝对路径，在该目录下创建业务的TestCase层代码
        :param case_info:
        :return: 创建成功之后的*.py文件的绝对路径
        """
        file_name_ = case_info['path'].replace('/', '_')
        template_file_name = f"test{file_name_}.py"
        conftest_file = "conftest.py"
        file_path = os.path.join(os.getcwd(), case_dest_directory)
        if os.path.isfile(file_path):
            os.remove(file_path)
        # 如果当前文件夹下对应path中提取的文件夹名称不存在，则创建该文件夹，并创建一个__init__.py文件
        case_dest_directory = case_dest_directory.strip("/")

        if "/" in case_dest_directory:
            dir_list = case_dest_directory.split("/")
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
            path = os.path.join(os.getcwd(), case_dest_directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(path + "/__init__.py", "w")
            else:
                if not os.path.exists(path + "/__init__.py"):
                    open(path + "/__init__.py", "w")

        # 如果*.py文件不存在的话，创建这个文件
        if not os.path.isfile(os.path.join(file_path, template_file_name)):
            f = open(os.path.join(file_path, template_file_name), "w", encoding='utf8')
            content = ''
        else:
            f = open(os.path.join(file_path, template_file_name), "r", encoding='utf8')
            content = f.read()
        conftest_file_path = os.path.join(file_path, conftest_file)
        if not os.path.isfile(conftest_file_path):
            f = open(conftest_file_path, "w", encoding='utf-8')
            # 写模版
            conftest_string = Template(CaseTemplate._conftest_strings)
            content = conftest_string.substitute()
            with open(conftest_file_path, 'a+') as f:
                f.write(content)
        return os.path.join(file_path, template_file_name), content
