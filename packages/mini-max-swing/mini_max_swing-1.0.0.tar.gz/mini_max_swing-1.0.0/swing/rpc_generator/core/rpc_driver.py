"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 14:01
@Author: xingyun
"""
import json
import os
import sys
import time
import requests
import traceback

from collections import defaultdict
from thriftpy2.rpc import make_client

from rpc_generator.plugins.importlib import util
from rpc_generator.plugins import importlib
from rpc_generator.plugins.thrift_hook import hook
from rpc_generator.utils.utils import Utils
from rpc_generator.plugins.log.logger import logger
from rpc_generator.utils.json_search import JsonSearch


class RPCDriver:
    def __init__(self, psm, service, business, client_path, data_path, branch='main', timezone=""):
        self.max_retry_times = 1
        self.max_delay = 5
        self.p_s_m = psm
        self.service = service
        self.branch = branch
        self.biz = business
        self.data_path = data_path
        self.env = Utils.get_env()

        self.root_path = os.path.dirname(os.path.dirname(os.path.dirname(client_path)))
        self.json_path = f"{self.root_path}/{self.data_path}/json/{self.biz}/{self.p_s_m}.json"
        self.tft_obj, self.idl_path = self.import_module(psm)  # 对thrift文件解析出来的service
        #  优先获取bedrock传过来的参数
        if 'bedrock' in os.environ:
            bedrock_value = os.environ['bedrock']
            bedrock_value_dict = json.loads(bedrock_value)
            if self.p_s_m == bedrock_value_dict['psm'] and 'podLIst' in bedrock_value_dict:
                pod_list = bedrock_value_dict.get('podLIst')
                if pod_list is not None:
                    self.host = pod_list[0].split(':')[0]
                    self.port = pod_list[0].split(':')[1]
                    logger.info(f'====get env from bedrock, podLIst: {pod_list},use ip:port is: {self.host}:{self.port}')
        else:
            # 调用服务发现进行获取ip+port
            self.env_lookup = Utils.get_conf("rpc_domains", f"{self.env}_{psm}_env")
            project_name = self.env_lookup.split("://")[0]
            cluster_name = self.env_lookup.split("cluster=")[1]
            psm_name = self.env_lookup.split('//')[1].split('?')[0]
            # 调用 服务发现 进行获取ip+port
            env_lookup_url = f"http://swing.xaminim.com/get/env_lookup?project_name={project_name}&cluster_name={cluster_name}&psm_name={psm_name}"
            env_info = requests.request("GET", env_lookup_url, verify=False)
            # print(f'\n=====get env_lookup: {env_info.json()}')
            if env_info.json()['result'] is not None:
                self.host = env_info.json()['result'].split(':')[0]
                self.port = int(env_info.json()['result'].split(':')[1])
                print(f'\n====get env from swing_server, ip:port is: {self.host}:{self.port}')
            else:
                # 兜底一下 conf配置兜底
                self.host = Utils.get_conf("rpc_domains", f"{self.env}_{psm}_host")
                self.port = int(Utils.get_conf("rpc_domains", f"{self.env}_{psm}_port"))
                logger.info(f'\n====get env from conf, ip:port is: {self.host}:{self.port}')

        # todo1 读取配置文件获取path& port
        # demo
        # self.content_service_thrift = thriftpy2.load(
        #    "/Users/minimax/PycharmProjects/pythonProject4/swing/data/idls/tns/content/content.thrift",
        #    module_name="content_service_thrift")
        # self.client = make_client(self.content_service_thrift.ContentService, "testnodeport.xaminim.com", 30554,
        #                          timeout=60000)
        service_name = getattr(self.tft_obj, service)  # 获取服务定义
        self.client = make_client(service_name, self.host, self.port, timeout=30000)
        self.client_path = client_path
        self.timezone = timezone
        self.root_path = os.path.dirname(os.path.dirname(os.path.dirname(client_path)))

    def import_module(self, psm):
        thrift_file = '_'.join(psm.split('.'))
        module_path = os.path.join(self.root_path, self.data_path, "idls", self.biz)

        if not os.path.exists(module_path):
            abs_path = os.path.abspath(sys.argv[0])
            root_path = os.path.dirname(os.path.dirname(os.path.dirname(abs_path)))
            module_path = os.path.join(root_path, self.data_path, "idls", self.biz)
        service_path = os.path.join(module_path, f"{thrift_file}_{self.service}")

        # 目标遍历目录
        target_path = module_path
        if os.path.isdir(service_path):
            target_path = service_path

        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file == f"{thrift_file}.thrift":
                    idls_index = root.split(os.sep).index("idls")
                    module = ".".join(root.split(os.sep)[idls_index - 1:])
                    idl_path = module_path + "/" + psm + "/" + file
                    # install_thrift_import_hook()
                    hook.install_thrift_import_hook()
                    obj = importlib.import_module(f"{module}.{thrift_file}_thrift")

                    return obj, idl_path
        raise FileNotFoundError("{thrift_file}.thrift not found!")

    def FindTypeInIncludes(self, part_name, _type, psm):
        try:
            req = getattr(self.tft_obj, _type)()
            return req
        except:
            p_s_m = '_'.join(psm.split('.'))
            idls_path = os.path.join(self.root_path, self.data_path, "idls", f"{part_name}", f"{p_s_m}")
            if not os.path.isdir(idls_path):
                try:
                    for path in sys.path:
                        idls_path = os.path.join(path, self.data_path, "idls", f"{part_name}", f"{p_s_m}")
                        if os.path.isdir(idls_path):
                            break
                except Exception as e:
                    logger.error('cannot find idls path for:', e)

            for root, dirs, files in os.walk(idls_path):
                for file in files:
                    if file.split('.')[-1] == "thrift" and file.split('.')[0] == _type.split('.')[0]:
                        path = (root + '/' + file)[:-7] + '_thrift'
                        obj = importlib.import_module(path)
                        try:
                            return getattr(obj, _type.split('.')[-1])()
                        except:
                            pass
            raise AttributeError

    def JungleValueIsInter(self, Key):
        """
        判断是list:[i32] 或<i32>类型
        """
        if len(Key) == 0:
            print("Key Error, the length of Key = 0")
            raise ValueError
        # key: "i32"
        if Key[0] == 'i' and Key[1:].isdigit():
            return True
        # list: "[i32]"
        if len(Key) >= 5 and Key[2] == 'i' and Key[3:4].isdigit():
            return True
        return False

    def JungleKey(self, key):
        """
        判断key是 <i32> 或<string>类型
        """
        if str(key)[0] == '<' and str(key)[-1] == '>':
            return True
        return False

    def set_base(self, request):
        base = defaultdict(dict, request.get("Base", {}))
        if base.get("Extra", {}).get("Env", {}) == {}:
            base['Extra']['Env'] = ""
        if base.get("TrafficEnv", {}).get("Env", {}) == {}:
            base['TrafficEnv']['Env'] = ""
        request["Base"] = base

    def get_req(self, request):
        """
        :desc:动态创建请求req
        :param request:ast解析后的json req
        :return: thrift req对象
        """
        if not isinstance(request, (list, dict)):
            return request

        if isinstance(request, list):
            if len(request) == 0:
                return dict()
            r = list()
            for _req in request:
                r.append(self.get_req(_req))
            return r

        # Base可以先忽略，统一处理Base，可以加快处理速度
        if request.get("__type") == "Base":
            return

        # 如果为dict，且只有__type一个key,不作构造处理
        if isinstance(request, dict) and len(request) == 1:
            for k, v in request.items():
                if k == "__type":
                    return

        # 获取请求的类型
        try:
            _req = self.FindTypeInIncludes(self.biz, request.get("__type"), self.p_s_m)
        except:
            # 主要针对map数据
            _req = {}
            for _key, _value in request.items():
                if len(str(_value)) > 1 and self.JungleValueIsInter(str(_value)):
                    _req = None
                    continue
                if len(str(_key)) > 2 and self.JungleKey(str(_key)):
                    _req = None
                    continue
                if str(_key).isdigit():
                    _key = int(_key)
                if _req is None:
                    _req = {}
                _req[_key] = None
                if isinstance(_value, dict):
                    ret = self.get_req(_value)
                else:
                    ret = _value
                _req[_key] = ret
        for key, value in request.items():
            if len(str(value)) > 1 and self.JungleValueIsInter(str(value)):
                continue
            if len(str(key)) > 2 and self.JungleKey(str(key)):
                continue
            # 如果请求是list类型，递归调用
            if isinstance(value, list):
                item_list = []
                for item in value:
                    # 处理list中是dict的情况
                    if isinstance(item, (dict, list)):
                        ret = self.get_req(item)
                        if ret:
                            item_list.append(ret)
                    else:
                        item_list.append(item)
                # setattr(req, key, item_list)
                if not isinstance(_req, dict):
                    setattr(_req, key, item_list)
                else:
                    _req[_key] = item_list
            else:
                # 如果json中的value是""，说明这个字段不需要，直接忽略，非空字段复制给req
                if key != "__type":
                    if value == " ":
                        value = ""
                    if isinstance(value, dict):
                        ret = self.get_req(value)
                        # setattr(req, key, ret)
                        if not isinstance(_req, dict):
                            setattr(_req, key, ret)
                        else:
                            _req[_key] = ret
                    else:
                        if not isinstance(_req, dict):
                            setattr(_req, key, value)
                        else:
                            _req[_key] = value
        return _req

    def get_base(self, _req=None, base_param='Base'):
        """
        :desc:统一处理base，给base加上logid
        :return:
        """
        if _req is None:
            _req = {}
        module_name = f"{self.data_path}.idls.base_thrift"
        sys.path.append(module_name)
        spec = importlib.util.find_spec(module_name)
        base_obj = ""
        if spec is not None:
            base_obj = importlib.import_module(module_name)
        # 获取请求数据中的原始Base信息
        base_info = getattr(_req, base_param, {}) or {}
        # 优先透传Base信息
        req_traffic = None
        if base_info.get('TrafficEnv', None):
            req_traffic = base_obj.TrafficEnv(
                Open=base_info.get('TrafficEnv', {}).get('Open', False),
                Env=base_info.get('TrafficEnv', {}).get('Env', ''),
            )
        base = base_obj.Base(
            TrafficEnv=req_traffic,
            Extra=base_info.get('Extra', None),
        )
        base.LogID = Utils.generate_trace_id()
        base.Caller = ""
        try:
            # 优先使用用户传入的Base信息，否则填充TrafficEnv
            if not base_info or not base_info.get('TrafficEnv', {}).get('Env', ''):
                traffic = base_obj.TrafficEnv(
                    Open=False,
                    Env='',
                )
                base.TrafficEnv = traffic
        except Exception as e:
            raise e

        return base

    def prn_req(self, req):
        """
        :desc:用于打印req
        :param req:
        :return:
        """
        try:
            req.pop("__type")
            req.pop("Base")
        except:
            pass
        return req

    def rpc_call(self, request, method):
        """
        :desc:根据动态构造的req，动态发送请求
        :param request:
        :param method:
        :return:
        """
        retry_time = 0
        for i in range(self.max_retry_times):
            try:
                req_ = self.get_req(request)
                # 补充logid参数
                # 发起调用
                logger.info(f"==={method} === request:{req_}")
                try:
                    res = getattr(self.client, method)(req_)
                    print("req is =======")
                    print(req_)
                    print("res is =======")
                    print(res)
                except Exception as e:
                    print(f'rpc call failed for:{e}')

                log_id = ''
                if 'base_resp' in JsonSearch(res).json:
                    if 'trace_info' in JsonSearch(res).json['base_resp']:
                        if JsonSearch(res).json['base_resp']['trace_info'] is not None:
                            if 'trace_id' in JsonSearch(res).json['base_resp']['trace_info']:
                                lod_id = JsonSearch(res).json['base_resp']['trace_info']['trace_id']
                                print('trace_id is=== :{}'.format(lod_id))
                return JsonSearch(res).json, log_id

            except Exception as e:
                retry_time += 1
                logger.error(f'rpc call failed for:{e}, retry {retry_time} times.')
                time.sleep(self.max_delay)
                logger.debug(f"rpc error, client:{self.client}, retry...")
                if retry_time == self.max_retry_times:
                    logger.error(traceback.format_exc())


class ThriftImportHook:
    def __init__(self, thrift_root):
        self.thrift_root = thrift_root

    def find_spec(self, fullname, path, target=None):
        # Only handle imports starting with "thrift_modules."
        if not fullname.startswith('thrift_modules.'):
            return None

        # Extract the Thrift module name from the full import name
        module_name = fullname[len('thrift_modules.'):]
        thrift_file = f'{module_name}.thrift'

        # Locate the Thrift IDL file within the thrift_root directory
        thrift_file_path = os.path.join(self.thrift_root, thrift_file)
        if not os.path.isfile(thrift_file_path):
            return None

        # Assuming the Thrift IDL file is valid and can be loaded
        # (you may need to implement actual Thrift parsing logic here)
        spec = importlib.util.spec_from_file_location(fullname, thrift_file_path)
        if spec is None:
            return None

        return spec


if __name__ == '__main__':
    # rpc_d = RPCDriver("ys_chat", "11", "111", "111", "data")
    # req = rpc_d.import_module("ys_chat")
    print(Utils.get_json_data('/Users/minimax/PycharmProjects/pythonProject5/swing/data/json/weaver/conversation_chat.json'))
