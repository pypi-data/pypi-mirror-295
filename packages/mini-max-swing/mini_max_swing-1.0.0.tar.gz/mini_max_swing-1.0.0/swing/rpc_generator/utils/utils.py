import os
import json
import sys
import time
import socket
# noinspection PyCompatibility
import urllib.parse
import uuid
import random
import configparser
import datetime
from rpc_generator.plugins.log.logger import logger


class Utils:
    @staticmethod
    def get_json_data(path):
        with open(path, 'r') as f:
            load_dict = json.load(f)
        return load_dict

    @staticmethod
    def get_domain(psm=None, cluster=None, env=None):
        # 优先从bedrock中获取env
        if 'bedrock' in os.environ:
            bedrock_value = os.environ['bedrock']
            bedrock_value_dict = json.loads(bedrock_value)
            if 'pod_list' in bedrock_value_dict:
                pod_list = bedrock_value_dict.get('pod_list')
                if pod_list is not None:
                    host = pod_list[0].split(':')[0]
                    port = pod_list[0].split(':')[1]
                    domain = f'{host}:{port}'
                    logger.info(f'====get env from bedrock, podLIst: {pod_list},use ip:port is: {host}:{port}')
        else:
            if len(cluster) > 0:
                domain = Utils.get_conf("http_domains", f"{env}_{psm}_{cluster}")
            else:
                domain = Utils.get_conf("http_domains", f"{env}_{psm}_domain")  # 从conf/conf.ini中获取请求domain
            logger.info(f'====get env from conf, domain is : {domain}')
        return domain

    @staticmethod
    def get_env():
        if 'bedrock' in os.environ:
            print(os.environ['bedrock'])
            if 'env' in json.loads(os.environ['bedrock']):
                return json.loads(os.environ['bedrock'])['env']
        return Utils.get_conf("common", "env")

    @staticmethod
    def get_env_label():
        if 'bedrock' in os.environ:
            if 'env_label' in json.loads(os.environ['bedrock']):
                return json.loads(os.environ['bedrock'])['env_label']

        return Utils.get_conf("common", "env_label")

    @staticmethod
    def generate_trace_id():
        date_part = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        local_ip = "1.2.3.4"
        try:
            local_ip = '192.168.0.12'
        except Exception as e:
            logger.warning(f"get local ip failed, error for {str(e)}")
        ip_part = "".join([x.zfill(3) for x in local_ip.split(".")])
        random_part = str(random.randint(10000, 99999))
        return date_part + ip_part + random_part

    @staticmethod
    def get_conf_abspath():
        runner_abspath_dirname = os.path.dirname(os.path.abspath(sys.argv[-1]))
        now_abspath_dirname = runner_abspath_dirname
        for i in range(5):
            for root, dirs, files in os.walk(now_abspath_dirname):
                if "conf" in dirs:
                    return now_abspath_dirname + "/conf/conf.ini"
            now_abspath_dirname = os.path.dirname(now_abspath_dirname)
        raise Exception("not found /conf/conf.ini")

    @staticmethod
    def get_nearest_conf(section, key):
        """
        获取最近的conf.ini
        """
        file = Utils.get_conf_abspath()
        config = configparser.ConfigParser()
        config.read(file)
        try:
            return config[section][key]
        except KeyError:
            raise KeyError(f"conf.ini, section:{section},key:{key} not found, please check!")

    @staticmethod
    def get_conf(section, key):
        if os.environ.get(key, None):
            return os.environ[key]
        else:
            file = Utils.get_conf_abspath()
            config = configparser.ConfigParser()
            config.read(file)
            try:
                return config[section][key]
            except KeyError:
                raise KeyError(f"conf.ini, section:{section},key:{key} not fould, please check!")

    @staticmethod
    def get_section_key():
        file = Utils.get_conf_abspath()
        try:
            config = configparser.ConfigParser()
            config.read(file)
            return config.sections()
        except KeyError:
            raise KeyError(f"The path {file} not fould, please check!")

    @staticmethod
    def get_git_conf(section, key):
        runner_abspath_dirname = os.path.dirname(os.path.abspath(__file__)).split('/utils')[0]
        now_abspath_dirname = runner_abspath_dirname
        for i in range(5):
            for root, dirs, files in os.walk(now_abspath_dirname):
                if "conf" in dirs:
                    file = now_abspath_dirname + "/conf/conf.ini"
                    return Utils.get_conf_from_ini(file, section, key)

    @staticmethod
    def parse_url_params(url):
        result = urllib.parse.urlsplit(url)
        params = dict(urllib.parse.parse_qsl(result.query))
        return result, params

    @staticmethod
    def get_conf_from_ini(file, section, key):
        config = configparser.ConfigParser()
        config.read(file)
        try:
            return config[section][key]
        except KeyError:
            raise KeyError(f"conf.ini, section:{section},key:{key} not fould, please check!")

    @staticmethod
    def write_json(json_data, json_path):
        with open(json_path, "w") as fp:
            fp.write(json.dumps(json_data, indent=4))

    @staticmethod
    def get_setup_conf(root, section, key):
        file = os.path.join(root, f"setup.ini")
        if os.path.isfile(file):
            config = configparser.ConfigParser()
            config.read(file)
            try:
                return config[section][key]
            except KeyError:
                raise KeyError(f"setup.ini, section:{section},key:{key} not fould, please check!")
        else:
            raise Exception(f"setup.ini file is not exist under project root path, please check!")

    @staticmethod
    def get_user():
        """
        获取本次使用工具的使用者
        :return:
        """
        r = os.popen("git config --list | grep user")
        text = r.read()
        r.close()
        if "user" in text:
            return text.rsplit("=", 1)[1].strip()
        else:
            return ""

    @staticmethod
    def get_now_timestamp():
        millis = int(round(time.time() * 1000))
        return millis

    @staticmethod
    def get_hostname():
        return socket.gethostname()

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
            s.close()
        finally:
            return ip

    @staticmethod
    def generate_build_no():
        return str(uuid.uuid1())

    @staticmethod
    def get_xray_impact_cases():
        cases_str = os.getenv("xray_impact_cases")
        if cases_str is None or len(cases_str) == 0:
            return []
        else:
            return cases_str.split(",")

    @staticmethod
    def update_json_(json_a, json_b):
        for key, value in json_a.items():
            if key in json_b:
                # 如果key在jsonB中存在，检查value的类型
                if isinstance(value, dict):
                    # 如果value是字典，递归调用update_json
                    Utils.update_json_(value, json_b[key])
                elif isinstance(value, list):
                    # 如果value是列表，检查jsonB中的对应值是否也是列表
                    if isinstance(json_b[key], list):
                        # 如果是列表，更新列表中的每个元素
                        for i, item in enumerate(value):
                            if i < len(json_b[key]):
                                # 如果jsonB中的列表长度足够，更新对应的元素
                                Utils.update_json_(item, json_b[key][i])
                            else:
                                # 如果jsonB中的列表长度不够，添加新的元素
                                json_b[key].append(item)
                    else:
                        # 如果jsonB中的值不是列表，替换整个列表
                        json_b[key] = value
                else:
                    # 如果value不是字典也不是列表，直接更新
                    json_b[key] = value
            else:
                # 如果key在jsonB中不存在，直接添加到jsonB
                json_b[key] = value
        return json_b


if __name__ == "__main__":
    bed_rock_string = '{"jobId":"job-mcfUIppg","operator":"雷蒙","psm":"wk-wwww","env":"prod","env_label":"main", "pod_list": ["10.32.130.11:8888"]}'

    bedrock_value_dict = json.loads(bed_rock_string)
    if 'pod_list' in bedrock_value_dict:
        pod_list = bedrock_value_dict.get('pod_list')
        if pod_list is not None:
            host_ = pod_list[0].split(':')[0]
            port_ = pod_list[0].split(':')[1]
            domain = f'{host_}:{port_}'
            logger.info(f'====get env from bedrock, podLIst: {pod_list},use ip:port is: {host_}:{port_}')
# print(Utils.generate_trace_id())
