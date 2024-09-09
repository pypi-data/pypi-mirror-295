"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:44
@Author: xingyun
"""

import os
from string import Template
from rpc_generator.utils.utils import Utils
from rpc_generator.plugins.log.logger import logger

service_string = """import sys
import os
from rpc_generator.core.rpc_driver import RPCDriver
from rpc_generator.core.base_service import BaseService



class $service_name(BaseService):
    def __init__(self):
        super().__init__(os.path.abspath(__file__), "$data_path")
        self.psm = "$psm"
        self.service = self.__class__.__name__
        self.business = self.get_dirname(__file__)
        self.branch = "$branch"
        self.path = os.path.abspath(__file__)  # 当前路径，用于定位配置文件
        self.rpc_driver = RPCDriver(psm=self.psm, service=self.service, business=self.business,
                                    client_path=self.path, data_path=self.data_path, branch=self.branch)
"""
decorator_string = """
    @xray_trace_rpc(psm="$psm", rpc="$method_name")"""
method_string = """
    def $method_name(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid
"""
test_string = """

if __name__ == "__main__":
    service = $service_name("sd://$psm?cluster=default")
"""
service_tmpl = Template(service_string)
method_tmpl = Template(method_string)
method_decorator_tmpl = Template(decorator_string + method_string)
test_tmpl = Template(test_string)


def gen_service(psm_service, branch, json_path, biz, data_path='data', module_path='modules', xray=""):
    psm = psm_service.split('@')[0]
    json_data = Utils.get_json_data(json_path)
    content = ''
    file_name = f"{'_'.join(psm_service.split('.')).replace('@', '_')}.py"
    file_path = os.path.join(os.getcwd(), module_path, biz, file_name)
    modules_path = os.path.join(os.getcwd(), module_path)
    if not os.path.exists(modules_path):
        os.makedirs(modules_path)
        with open(os.path.join(modules_path, '__init__.py'), 'w') as f:
            f.close()
    if os.path.isfile(file_path):
        print(f"psm:{psm} moudle file has alredy exist")
    else:
        logger.info(f"begin to gen moudle file {file_name}")
        if not os.path.exists(os.path.join(os.getcwd(), module_path, biz)):
            os.makedirs(os.path.join(os.getcwd(), module_path, biz))
            with open(os.path.join(os.getcwd(), module_path, biz, "__init__.py"), 'w') as f:
                f.close()
        service_name = json_data["result"][0]["service_name"]
        content += service_tmpl.substitute({"service_name": service_name, "psm": psm, "data_path": data_path, "branch": branch})
        for method in json_data["result"][0]["method"]:
            if xray:
                content += method_decorator_tmpl.substitute({"method_name": method["name"], "psm": psm})
            else:
                content += method_tmpl.substitute({"method_name": method["name"], "psm": psm})
        content += test_tmpl.substitute({"service_name": service_name, "psm": psm})
        with open(file_path, 'w') as f:
            f.write(content)
        logger.info(f"gen moudle file {file_name} successful")
    return file_path
