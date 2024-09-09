"""
coding:utf-8
@Software: PyCharm
@Time: 2024/5/12 11:59
@Author: xingyun
"""
import logging
import os
from string import Template
from swing.rpc_generator.plugins.log.logger import logger


class ConfTemplate(object):
    _conf_string = """
[common]
# env：运行环境 支持：all，prod，pre，test
env = prod 
env_label = prod

[rpc_domains]
pre_{{psm_name}}_host = testnodeport.xaminim.com
prod_conversation_chat_host = testnodeport.xaminim.com
prod_conversation_chat_port= xxx
test_conversation_chat_host = xxx

[http_domains]
pre_{{psm_name}}_domain = testnodeport.xaminim.com
prod_ys_chat_domain = testnodeport.xaminim.com
test_ys_chat_domain = xxxxxx


[log_domains]
general_url = https://loki-query-aliprod.xaminim.com/loki/api/v1/query_range
pre_general_host = xxxx
test_general_app = xxxxx
min_minute = 5

[report_message]
prod_report_title = 线上环境巡检
pre_report_title = 预发环境选件
prod_report_scene = 开放平台线上环境接口自动化巡检
pre_report_scene = 开放平台预发环境接口自动化巡检
    """

    def __init__(self):
        pass

    def generate_template(self, conf_dest_directory=None):
        """
        生成模板方法
        :param conf_dest_directory: 生成数据模板的路径
        :return:
        """
        if not conf_dest_directory:
            conf_dest_directory = "conf"
        else:
            conf_dest_directory = f"conf/{conf_dest_directory}"
        abs_conf_path = os.path.join(os.getcwd(), conf_dest_directory)
        if not os.path.exists(abs_conf_path):
            conf_file_path = ConfTemplate.create_conf_file(conf_dest_directory)
            print("生成数据模板的路径为 :", conf_file_path)
            if conf_file_path:
                logging.info("创建数据文件成功!")
            else:
                logging.warning("创建数据文件失败!")
                return
            # 根据模版写入conf
            service_tmp_string = Template(ConfTemplate._conf_string)
            content = service_tmp_string.substitute()
            with open(conf_file_path, 'a+') as f:
                f.write(content)
            logging.info(f"set conf file {conf_file_path} successful")

    @staticmethod
    def create_conf_file(conf_dest_directory=None):
        """
        根据psm名称创建目录文件
        :param conf_dest_directory: 生成数据模板的目标绝对路径
        :return: 创建成功之后的*.py文件的绝对路径
        """
        if not conf_dest_directory:
            conf_dest_directory = "conf"
        conf_name = "conf.ini"
        # 如果当前文件夹下对应path中提取的文件夹名称不存在，则创建该文件夹，并创建一个__init__.py文件
        if conf_dest_directory.startswith("/"):
            conf_dest_directory = conf_dest_directory[1:]
        if conf_dest_directory.endswith("/"):
            conf_dest_directory = conf_dest_directory[:-1]
        file_path = os.path.join(os.getcwd(), conf_dest_directory)

        if "/" in conf_dest_directory:
            dir_list = conf_dest_directory.split("/")
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
            path = os.path.join(os.getcwd(), conf_dest_directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(path + "/__init__.py", "w")
            else:
                if not os.path.exists(path + "/__init__.py"):
                    open(path + "/__init__.py", "w")
        conf_file_path = os.path.join(file_path, conf_name)
        logger.info(f"gen conf file {conf_file_path} successful")
        # 如果conf.ini文件不存在的话，创建这个文件
        if not os.path.isfile(conf_file_path):
            open(conf_file_path, "w", encoding='utf8')

        return conf_file_path


if __name__ == '__main__':
    conf_path = "conf/"
    ConfTemplate.create_conf_file()

