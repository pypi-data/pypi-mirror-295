"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:41
@Author: xingyun
"""
import os
import re
from string import Template
from swing.rpc_generator.utils.utils import Utils
from swing.rpc_generator.plugins.log.logger import logger

service_string = '''import pytest
from $package_path import $service_name
from swing.common.common import Common


class Test$service_name(object):
'''

method_string = '''    def test_$method_name(self):
        """
        用例描述：测试 $method_name 接口正常情况
        """
        caseparam = {
            "env": "all",
            "rpc_method": $service_name().$method_name,
            "rpc_param": {
                "xxx你的参数填在这里xxxx": ""
            },
            "expect": {
                "stcAssertPart": {
                    "xxxx 你的结果断言写在这里": ""
                }
            },
            # 不需要日志断言 可以去掉
            "log_assert": {
                "xxxx 你的日志断言写在这里": ""
            }
        }
        Common.api_handle(caseparam)       

'''

service_tmpl = Template(service_string)
method_tmpl = Template(method_string)


def gen_case(psm_service, json_path, biz, modules_path="modules", case_path='rpc_cases'):
    psm = psm_service.split('@')[0]
    json_data = Utils.get_json_data(json_path)
    for key in json_data['result'][0]['method']:
        content = ''
        method_name = re.sub(r'(?<!^)(?=[A-Z])', '_', key['name']).lower()
        method_name_ = f"test_{method_name}.py"

        file_name = f"{'_'.join(psm_service.split('.')).replace('@', '_')}"
        file_path = os.path.join(os.getcwd(), case_path, biz, file_name, method_name_)
        cases_path = os.path.join(os.getcwd(), case_path)
        if not os.path.exists(cases_path):
            os.makedirs(cases_path)
            with open(os.path.join(cases_path, '__init__.py'), 'w') as f:
                f.close()
        if os.path.isfile(file_path):
            logger.info(f"psm:{psm} case file has alredy exist")
        else:
            logger.info(f"begin to gen case file {file_path}")
            if not os.path.exists(os.path.join(os.getcwd(), case_path, biz)):
                os.makedirs(os.path.join(os.getcwd(), case_path, biz))
                with open(os.path.join(os.getcwd(), case_path, biz, "__init__.py"), 'w') as f:
                    f.close()
            service_name = json_data["result"][0]["service_name"]
            package_path = "{}.{}.{}".format(modules_path, biz, '_'.join(psm_service.split('.')).replace('@', '_'))
            content += service_tmpl.substitute({"package_path": package_path, "service_name": service_name})
            refresh = key['request_json']
            def_name = key['name']
            content += method_tmpl.substitute(
                {"method_name": def_name, "service_name": service_name, "refresh": refresh})

            if not os.path.exists(os.path.join(os.getcwd(), case_path, biz, file_name)):
                os.makedirs(os.path.join(os.getcwd(), case_path, biz, file_name))
                with open(os.path.join(os.getcwd(), case_path, biz, file_name, "__init__.py"), 'w') as f:
                    f.close()
            if not os.path.isfile(file_path):
                f = open(file_path, "w", encoding='utf8')
                f.write(content)
                f.close()

                logger.info(f"gen case file {file_path} successful")
