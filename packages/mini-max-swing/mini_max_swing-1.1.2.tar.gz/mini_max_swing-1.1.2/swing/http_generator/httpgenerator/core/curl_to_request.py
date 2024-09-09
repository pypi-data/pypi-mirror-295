"""
coding:utf-8
@Software: PyCharm
@Time: 2024/5/14 17:21
@Author: xingyun
"""
import json
import logging
import pandas as pd

from urllib.parse import parse_qs, urlparse

key_list = ['header', 'method', 'path', 'req_schema', 'body_param', 'query_param', 'files', 'form_data']


class CurlToRequest:
    @staticmethod
    def parse_curls_from_csv(csv_path):
        data = pd.read_csv(csv_path)
        curl_list = data['curl'].tolist()

        result_list = []
        for curl in curl_list:
            result = CurlToRequest.parse_curl_command(curl)
            result_list.append(result)
        logging.info(f'======== parse_curls_from_csv_result is ========\n {result_list}')
        return result_list

    @staticmethod
    def parse_curl_command(curl_command, flag=None, update_key_value=None):
        """
        : param curl_command str:
        : param flag: bool // 是否需要替换参数
        : param update_key_value: list // 需要替换的value{"header": {"token": "xxxx","qa_tag": "qa_test"}, "query": {"did": 123455}}
        """
        # print('curl_command\n', curl_command)
        # 解析headers
        headers = {}
        header_str = curl_command.split('curl ')[1].split('--data-binary')[0].strip()
        header_lines = header_str.split(' -H ')
        for line in header_lines:
            if line.startswith('"'):
                key_value = line.strip('"').split(': ', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    headers[key] = value
        # 解析请求体
        data = curl_command.split('--data-binary')[1].split('--compressed')[0].strip(' "')
        # logging.info('The data is {}'.format(data))
        # 判断字符串中是否包含 '\'
        if '\\' in data:
            # 替换所有的 \" 为 "
            data = data.replace('\\"', '"')
        data = json.loads(data)
        # 解析URL和query参数
        url = curl_command.split('--compressed ')[1].strip('"')
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        # 对query_params进行处理
        query_params = {key: value[0] for key, value in query_params.items()}
        # 构造结果结构体
        result = {
            'url': parsed_url.geturl().split('?')[0],
            'header': CurlToRequest.get_param_info(headers),
            'method': 'POST',
            'path': parsed_url.path,
            'req_schema': {
                'body_param': CurlToRequest.get_properties_from_schema(data),
                # 'query_params': {k: v[0] for k, v in query_params.items()},
                'query_param': CurlToRequest.get_param_info(query_params),
                "files": {},
                "form_data": {}
            },
            'resp_schema': {}
        }

        # 在返回前判断业务是否需要添加或者更新
        if flag:
            assert update_key_value is not None, f'flag is True but update_key_value is None'
            return CurlToRequest.update_params(update_key_value, result)

        # print(json.dumps(result, indent=4, ensure_ascii=False))
        return result

    @staticmethod
    def update_params(change_key, origin_result):
        if not isinstance(change_key, dict):
            raise TypeError(f'change_key: {change_key} is not dict')
        for key, value in change_key.items():
            if isinstance(value, dict):
                assert key in key_list, f'key {key} not in origin_result'
            if key in origin_result:
                # 如果key在jsonB中存在，检查value的类型
                if isinstance(value, dict):
                    # 如果value是字典，递归调用update_json
                    CurlToRequest.update_params(value, origin_result[key])
                elif isinstance(value, list):
                    # 如果value是列表，检查jsonB中的对应值是否也是列表
                    if isinstance(origin_result[key], list):
                        # 如果是列表，更新列表中的每个元素
                        for i, item in enumerate(value):
                            if i < len(origin_result[key]):
                                # 如果jsonB中的列表长度足够，更新对应的元素
                                CurlToRequest.update_params(item, origin_result[key][i])
                            else:
                                # 如果jsonB中的列表长度不够，添加新的元素
                                origin_result[key].append(item)
                    else:
                        # 如果jsonB中的值不是列表，替换整个列表
                        origin_result[key] = CurlToRequest.update_key(value)
                else:
                    # 如果value不是字典也不是列表，直接更新
                    origin_result[key] = CurlToRequest.update_key(value)

            else:
                # 如果key在jsonB中不存在，直接添加到jsonB
                origin_result[key] = CurlToRequest.update_key(value)
        return origin_result

    @staticmethod
    def get_param_info(params):
        params_info = {}
        for param in params:
            param_info = {
                'type': 'string',
                'optional': True,
                'children': {},
                'example': params[param]
            }
            params_info[param] = param_info
            # 如果有子参数，可以在这里添加
            # param_info['children'] = CurlToRequest.get_properties_from_schema(params[param])
        # print('The param_info is {}'.format(params_info))
        return params_info

    @staticmethod
    def get_properties_from_schema(body_params):
        body_params_info = {}
        for body_param, value in body_params.items():
            children = CurlToRequest.get_properties_from_schema(value) if isinstance(value, dict) else {}
            prop_info = {
                'type': type(value).__name__,
                'optional': True,
                'children': children,
                'example': value
            }
            body_params_info[body_param] = prop_info
        return body_params_info

    @staticmethod
    def update_key(value):
        origin_info = {
            "type": type(value).__name__,
            'optional': True,
            'children': {},
            'example': value
        }
        return origin_info


if __name__ == '__main__':
    # curl_com = """
    # curl -H "Host: api.xingyeai.com" -H "content-type: application/json" -H "x-timestamp: 1723258436" -H "accept: */*" -H "baggage: sentry-environment=release,sentry-public_key=e6b22d28b0ce98b16ce96cfd32d98c7b,sentry-release=1.32.000,sentry-sampled=false,sentry-trace_id=451822efe84546f19c4bece85edf5760,sentry-transaction=xingye.ChatViewController.leftButtonClick" -H "x-sign: 68039df6578b3fc88f480088156e9971ad9ed7b9" -H "x-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOjYwMCwiYWNjb3VudF9pZCI6OTMzNjgwMTU5NTgyMDMsImRldmljZV9pZCI6NDkyNDE5NzE5MDg3MjcsImlzX2Fub255bW91cyI6ZmFsc2UsImlzcyI6IndlYXZlcl9hY2NvdW50IiwiZXhwIjoxNzIzODYzMTgxLCJuYmYiOjE3MjMyNTgzODB9.T5NXarKzchHSntRBokFbm1kNxaNBSyXEZH9a2IoOdoc" -H "accept-language: zh-CN,zh-Hans;q=0.9" -H "sentry-trace: 451822efe84546f19c4bece85edf5760-e6904863674e4b5c-0" -H "sys_region: US" -H "user-agent: xingye/1124 CFNetwork/1335.0.3 Darwin/21.6.0" -H "ip_region: cn" --data-binary "{\"banner_scene\":3}" --compressed "https://api.xingyeai.com/weaver/api/v1/user/get_banner?appCode=&app_id=600&brand=apple&device_id=49241971908727&device_platform=ios&disable_personalization=0&idfa=&idfv=4EAEDA19-07DA-4042-A7F3-BCED788B06A3&ip_region=cn&is_anonymous=0&network_type=WIFI&os=1&os_version=15.6.1&request_lib=native&sys_language=zh-Hans-US&sys_region=US&timezone_offset=28800&user_id=93368015958203&user_mode=0&version_code=1320000&version_name=1.32.000"
    #    """

    curl_com = """
    curl -H "Host: api.xingyeai.com"  -H "content-type: application/json" -H "x-timestamp: 1723692509" -H "accept: */*" -H "baggage: sentry-environment=release,sentry-public_key=e6b22d28b0ce98b16ce96cfd32d98c7b,sentry-release=1.34.000,sentry-sampled=false,sentry-trace_id=9894de85a80d4d5aa87ba589a923be4b,sentry-transaction=HomePageViewController"  -H "accept-language: zh-CN,zh-Hans;q=0.9" -H "sentry-trace: 9894de85a80d4d5aa87ba589a923be4b-5dd90ecb7df0427c-0" -H "sys_region: CN" -H "user-agent: xingye/1135 CFNetwork/1402.0.8 Darwin/22.2.0" -H "ip_region: cn" --data-binary "{\"is_cold_start\":true,\"vip\":0,\"page\":0}" --compressed "https://api.xingyeai.com/weaver/api/v1/feed/get_explore_feed?appCode=&app_id=600&brand=apple&device_id=140165291921479&device_platform=ios&disable_personalization=0&idfa=&idfv=5D8AEA00-29C0-4A5F-ADA5-8818D787BA95&ip_region=cn&is_anonymous=0&network_type=WIFI&os=1&os_version=16.2&request_lib=native&sys_language=zh-Hans-CN&sys_region=CN&timezone_offset=28800&user_id=140162128294101&user_mode=0&version_code=1340000&version_name=1.34.000"
    """

    change_valur = {"header": {"x-tokens": "xxxx", "x-sign": "qa_test", "qa_tag": "qa_test"},
                    "req_schema": {"query_param": {"did": 123455}}}
    curl_result = CurlToRequest.parse_curl_command(curl_com, flag=True, update_key_value=change_valur)
    print(curl_result)
