"""
coding:utf-8
@Software: PyCharm
@Time: 2024/7/29 下午5:10
@Author: xingyun
"""
import importlib.util
import json
import os
import sys
import requests
import time
from datetime import datetime, timezone, timedelta

from swing.rpc_generator.utils.utils import Utils


class LogAssert:
    def __init__(self, grafana_info):
        """
        :param grafana_info:['use_cluster', 'name_space', 'app_name', 'query_name', 'from_time', 'to_time', 'assert_function',
                     'assert_key', 'retry_time', 'sleep_time', 'max_retries']
                     必传：use_cluster、name_space、app_name、query_name
                     非必传：from_time(默认30S)、to_time(now)、assert_function、assert_key、retry_time(重试的sleep时间，默认sleep 10s)、
                     sleep_time(第一次sleep时间，默认30s)，max_retries(重试次数， 默认5次)
        """
        print('********************************************** Log Assert 调试日志 ************************************')
        self.grafana_info = grafana_info
        if len(grafana_info) == 0 or (not isinstance(grafana_info, dict)):
            raise ValueError(f"输入的caseparam无效")
        key_param = ['use_cluster', 'name_space', 'app_name', 'query_name', 'from_time', 'to_time', 'assert_function',
                     'assert_key', 'retry_time', 'sleep_time', 'max_retries']
        for key in grafana_info:
            if key not in key_param:
                raise ValueError(f'输入的参数有误或暂未支持，失败入参：{key}')
        try:
            # 获取用户自定义参数
            self.use_cluster = grafana_info['use_cluster']
            self.name_space = grafana_info["name_space"]
            self.app_name = grafana_info["app_name"]
            self.query_name = grafana_info["query_name"]
            self.assert_function = grafana_info.get("assert_function", '')
            self.assert_key = grafana_info.get("assert_key", '')
            # 等待时间
            self.sleep_time = int(grafana_info.get("sleep_time", 30))
            time.sleep(self.sleep_time)
            self.max_retries = grafana_info.get("max_retries", 5)
            self.retry_delay = grafana_info.get("retry_time", 10)

        except Exception as e:
            print('get log_info params error, error is :', e)

    def log_assert(self):
        # 先获取grafana的返回结果
        grafana_resp = self.post_grafana_new()

        # 调用assert_function函数
        if grafana_resp is None:
            assert False, 'grafana_resp is None'
        # 获取function地址 进行调用
        if self.assert_function != '':
            print('=== start get lib_path =====')
            lib_path, lib_file_path = self.get_lib_path()
            print('=== get lib_path succ , lib_func_path is :', lib_file_path)
            # 开始调用
            print('==== start dynamic_import_and_use_function ====')
            if len(self.assert_function.split('.')) == 3:
                class_name = self.assert_function.split('.')[1]
                function_name = self.assert_function.split('.')[2]
                print(f'==== start execute {class_name} =====')
                # 创建类的实例并调用方法
                assert_class = LogAssert.dynamic_import_and_use_function(lib_file_path, class_name)
                if self.assert_key != '':
                    print(f'====assert_key is not empty, assert_key is :f{self.assert_key}  ====')
                    assert_instance = assert_class(grafana_resp, self.assert_key)
                else:
                    assert_instance = assert_class(grafana_resp)
                print(f'==== start excute function, function_name is:{function_name} =====')
                method_to_call = getattr(assert_instance, function_name)
                method_to_call()
                return ''
            assert False, f'assert_function is vaild, assert_function is {self.assert_function}'
        return grafana_resp

    def post_grafana_new(self):
        new_grafana_url = "https://mlogs.xaminim.com/api/v1/query"
        query_base = f"_namespace_:\"{self.name_space}\" and app:\"{self.app_name}\""
        query = query_base + " " + " ".join([f'and msg:\"{query_name}\"' for query_name in self.query_name])

        # 格式化为 ISO 8601 格式的字符串，包含微秒和时区信息
        from_formatted_time = (datetime.now(timezone(timedelta(hours=8))) - timedelta(hours=2)).isoformat()
        from_time = self.grafana_info.get("from_time", from_formatted_time)

        last_response = ""
        for attempt in range(self.max_retries):
            to_time = self.grafana_info.get("to_time", datetime.now(timezone(timedelta(hours=8))).isoformat())
            data = {
                "from": from_time,
                "to": to_time,
                "query": query,
                "limit": 10,
                "topic_name": f"_mlogs_{self.use_cluster}/{self.name_space}"
            }

            grafana_resp = requests.post(new_grafana_url, json=data)
            last_response = grafana_resp.text
            print(f"last_response:{last_response}")
            if grafana_resp.status_code == 200 and grafana_resp.json().get('data', {}).get('total', 0) != 0:
                return grafana_resp

            print(f'Attempt {attempt + 1} failed, retrying in {self.retry_delay} seconds...')
            time.sleep(self.retry_delay)

        print(f'Failed after {self.max_retries} attempts. Last response: {last_response}')
        return None

    def get_lib_path(self) -> str:
        lib_file = self.assert_function.split(".")[0]
        runner_abspath_dirname = os.path.dirname(os.path.abspath(sys.argv[-1]))
        now_abspath_dirname = runner_abspath_dirname
        for i in range(5):
            for root, dirs, files in os.walk(now_abspath_dirname):
                if "lib" in dirs:
                    return now_abspath_dirname + "/lib", now_abspath_dirname + "/lib/" + lib_file + '.py'
            now_abspath_dirname = os.path.dirname(now_abspath_dirname)
        return "", ""

    @staticmethod
    def dynamic_import_and_use_function(py_file_path, type_name):
        # 检查文件路径是否指向一个有效的Python文件
        if not py_file_path.endswith('.py'):
            raise ValueError("提供的路径不是有效的Python文件")
        # 将文件路径转换为模块名（去掉.py扩展名）
        module_name = py_file_path[:-3]
        # 构建模块的spec
        spec = importlib.util.spec_from_file_location(module_name, py_file_path)
        if spec is None:
            raise ImportError("无法加载模块")
        # 根据spec动态加载模块
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        # 执行模块的加载
        spec.loader.exec_module(module)
        # 从模块中获取指定的函数
        entity = getattr(module, type_name)
        return entity

    @staticmethod
    def get_grafana_function_play(resp):
        resp_json = resp.json()
        str_ = resp_json["data"]["items"][0]['msg']
        list_ = str_.split("----")
        for item in list_:
            if "function: Play" in item:
                list02 = item.split("- req:")
                list03 = list02[1].split("- resp:")
                # print("play方法的resp为", list03[1])
                list_aid = list03[0].split('"meta":')
                list_json_aid = list_aid[1][:-3]
                list04 = list03[0].split('"data_value":"')
                list05 = list04[1].split('","data_type":1}')
                play_req = list05[0].replace('\\', '')
                play_req_dict = json.loads(play_req)
                return play_req_dict, list_json_aid


if __name__ == '__main__':
    log_assert = {
        "use_cluster": "tx-shanghai-prod-02",
        "name_space": "xingye-prod",
        "app_name": "weaver-langnet-rpc",
        "query_name": ['66d95167000000005ca0c6ee9d169778', "180080716800243", "150060618744036"],
        # 'sleep_time':
        # 'assert_function': "prompt_assert.PromptAssert.model_assert",
        # "assert_key": (prompt_assert, aid, model_version)
    }
    grafana_resp_ = LogAssert(log_assert).post_grafana_new()
    req = LogAssert.get_grafana_function_play(grafana_resp_)
    print(req)
