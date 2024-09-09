"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
"""

import json
import os
import socket
import sys
import time
import uuid
from swing.http_generator.httpgenerator.utils.config_parse import ConfigParse
from swing.rpc_generator.plugins.log.logger import logger


class Utils(object):
    @staticmethod
    def write_json(json_data, json_path):
        with open(json_path, "w") as fp:
            fp.write(json.dumps(json_data, indent=4))

    @staticmethod
    def get_conf(section, key):
        # 从conf中获取业务线配置的domain
        # 获取当前业务线名称
        # 命令行获取 :testcase/doukai/aweme_open_biz_plaza/fans/test_fans_list.py
        try:
            dri_name = sys.argv[1].split('testcase/')[1].split("/")[0]
            root_path = os.getcwd()
        except:
            try:
                # 编译器全路径获取
                dri_name = os.getcwd().split("testcase/")[1].split('/')[0]
                root_path = os.getcwd().split("/testcase")[0]
            except:
                raise KeyError(f"conf path not found, please check!")
                # 判断是否是通用conf
        file = os.path.join(root_path, "conf", dri_name, f"conf.ini")
        config = ConfigParse()
        config.read(file)
        try:
            return config[section][key]
        except KeyError:
            raise KeyError(f"conf.ini, section:{section},key:{key} not found, please check!")

    @staticmethod
    def get_header_conf(section):
        file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "conf", f"conf.ini")
        config = ConfigParse()
        config.read(file)
        return dict(config._sections)[section]

    @staticmethod
    def get_env(psm=None, cluster=None, env=None):
        # 优先从bedrock中获取env
        if 'bedrock' in os.environ:
            bedrock_value = os.environ['bedrock']
            bedrock_value_dict = json.loads(bedrock_value)
            if psm == bedrock_value_dict['psm'] and 'podLIst' in bedrock_value_dict:
                pod_list = bedrock_value_dict.get('podLIst')
                if pod_list is not None:
                    host = pod_list[0].split(':')[1]
                    port = pod_list[0].split(':')[2]
                    domain = f'{host}:{port}'
                    logger.info(f'====get env from bedrock, podLIst: {pod_list},use ip:port is: {host}:{port}')
        else:
            if len(cluster) > 0:
                domain = Utils.get_conf("http_domains", f"{env}_{psm}_{cluster}")
            else:
                domain = Utils.get_conf("http_domains", f"{env}_{psm}_domain")    # 从conf/conf.ini中获取请求domain
            logger.info(f'====get env from conf, domain is : {domain}')
        return domain

    @staticmethod
    def get_env_label():
        if os.getenv("ENV_LABEL"):
            return os.getenv("ENV_LABEL")
        else:
            try:
                return Utils.get_conf("common", "env_label")
            except KeyError:
                return None

    @staticmethod
    def get_now_timestamp():
        millis = int(round(time.time() * 1000))
        return millis

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def generate_build_no():
        return str(uuid.uuid1())

    @staticmethod
    def get_ip():
        """
        查询本机ip地址
        :return: ip
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            return ip

    @staticmethod
    def get_user():
        '''
        获取本次使用工具的使用者
        :return:
        '''
        r = os.popen("git config --list | grep user")
        text = r.read()
        r.close()
        if "user" in text:
            return text.rsplit("=", 1)[1].strip()
        else:
            return ""


