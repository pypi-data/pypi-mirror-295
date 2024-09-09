#!/usr/bin/python
"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:41
@Author: xingyun
"""
import os
import argparse
import configparser
from rpc_generator.plugins.log.logger import logger
from rpc_generator.core.psm_files import PsmFiles


class RpcGenerator(object):
    def __init__(self, branch="main", data_path="data", module_path="modules", psm=None, case_path="rpc_cases", xray=None):
        self.branch = branch
        self.data_path = data_path
        self.module_path = module_path
        self.case_path = case_path
        self.xray = xray

    def generate_rpc(self, psm=None):
        here = os.getcwd()
        # 判断是否有配置文件存在
        file = os.path.join(here, "setup.ini")
        if not os.path.isfile(file):
            logger.info(
                "setup.ini file is required to generate thrift files, for more information please refer to README.md")
            with open(file, 'w') as f:
                f.close()
            logger.info(
                "setup.ini file has created in the root directory, please configure the file according to README.md")
            return

        branch, data_path, module_path, conf_path, psm, xray, case_path = self.branch, self.data_path, self.module_path, self.case_path, psm, self.xray, self.case_path
        if os.sep in data_path or os.sep in module_path:
            logger.error("data_path or module_path only support first level directory, such like --data_path=datas")
            return

        config = ConfigParserUper()
        config.read(file)
        flag = False
        # 命令行输入某一服务
        if psm:
            for biz in config.sections():
                for psm_service in config[biz]:
                    if psm == psm_service:
                        PsmFiles.generate(psm_service, config[biz][psm_service], biz, branch, data_path, module_path,
                                          case_path, conf_path, True, xray)
                        flag = True
                    else:
                        continue
            if not flag:
                logger.error("psm not found in setup.ini, please check it!")
                return
        # 获取所有配置文件的服务
        else:
            for biz in config.sections():
                for psm_service in config[biz]:
                    PsmFiles.generate(psm_service, config[biz][psm_service], biz, branch, data_path, module_path, case_path, conf_path,
                                      True, xray)


class ConfigParserUper(configparser.ConfigParser):
    def __init__(self):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr: str) -> str:
        return optionstr


if __name__ == '__main__':
    RpcGenerator().generate_rpc()
