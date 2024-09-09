import json
import logging
import time

import pytest
import re

from rpc_generator.utils.utils import Utils
from requests_toolbelt import MultipartEncoder
from types import MethodType
from collections import Counter
from urllib.parse import urlencode
from common.log_assert import LogAssert


class Common(object):
    @staticmethod
    def api_request(caseparam):
        """
        使用场景：接口入参的参数读取和接口请求发送
        :param caseparam: json格式的用例参数配置
        :return: json格式的请求响应结果
        """
        # API接口入参
        refresh = {}
        # 上传的是否是文件类型
        form_flag = False
        stream = False
        if 'form_data' in caseparam:
            form_data = Common.api_stc_param(caseparam['form_data'])
            if len(form_data) == 0 or (not isinstance(form_data, dict)):
                raise ValueError(f"输入的form_data参数无效")
            form_flag = True
            if caseparam["headers"]['Content-Type'] == "multipart/form-data":
                refresh['form_data'] = MultipartEncoder(fields=form_data)
            elif caseparam["headers"]['Content-Type'] == "application/x-www-form-urlencoded":
                refresh['form_data'] = urlencode(form_data)

        if 'headers' in caseparam:
            headers = Common.api_stc_param(caseparam['headers'])
            if len(headers) == 0 or (not isinstance(headers, dict)):
                raise ValueError(f"输入的headers参数无效")
            if form_flag and headers['Content-Type'] == "multipart/form-data":
                headers['Content-Type'] = refresh['form_data'].content_type
            refresh['headers'] = headers

        if 'query_param' in caseparam:
            query_param = Common.api_stc_param(caseparam['query_param'])
            if len(query_param) == 0 or (not isinstance(query_param, dict)):
                raise ValueError(f"输入的query_param参数无效")
            refresh['query_param'] = query_param

        if 'body_param' in caseparam:
            body_param = Common.api_stc_param(caseparam['body_param'])
            if len(body_param) == 0 or (not isinstance(body_param, dict)):
                raise ValueError(f"输入的body_param参数无效")
            refresh['body_param'] = body_param

        # 是否打印日志，默认debug值为False即不打印日志
        if 'debug' in caseparam:
            if not isinstance(caseparam['debug'], bool):
                raise ValueError(f"输入的debug参数无效")
            debug = caseparam['debug']
        else:
            debug = False
        if 'stream' in caseparam:
            stream = caseparam['stream']

        # API接口调用
        if 'api_method' in caseparam:
            if not isinstance(caseparam['api_method'], MethodType):
                raise ValueError(f"输入的api_method参数无效")
            resp = Common.api_invoke(caseparam['api_method'], refresh_data=refresh, debug=debug, form_flag=form_flag,
                                     stream=stream)
        else:
            raise ValueError(f'请输入对应的API接口测试方法')

        return resp

    @staticmethod
    def rpc_request(caseparam):
        """
        使用场景：rpc接口入参的参数读取和接口请求发送
        :param caseparam: json格式的用例参数配置
        :return: json格式的请求响应结果
        """
        # RPC接口入参
        refresh = {}
        if 'rpc_param' in caseparam:
            rpc_param = Common.api_stc_param(caseparam['rpc_param'])
            if len(rpc_param) == 0 or (not isinstance(rpc_param, dict)):
                raise ValueError(f"输入的rpc_param参数无效")
            refresh = rpc_param

        # 是否打印日志，默认debug值为False即不打印日志
        if 'debug' in caseparam:
            if not isinstance(caseparam['debug'], bool):
                raise ValueError(f"输入的debug参数无效")
            debug = caseparam['debug']
        else:
            debug = False

        # RPC接口调用
        if 'rpc_method' in caseparam:
            if not isinstance(caseparam['rpc_method'], MethodType):
                raise ValueError(f"输入的rpc_method参数无效")
            resp = Common.rpc_invoke(caseparam['rpc_method'], refresh=refresh, debug=debug)
        else:
            raise ValueError(f'请输入对应的RPC接口测试方法')
        return resp

    @staticmethod
    def api_handle(caseparam, post_action=""):
        """
        使用场景：STC智能校验方法
        :param caseparam: json格式的用例参数配置
        :param post_action: 需要的返回值的key，默认是空，可配置string和list类型，其中，need_keys配置为string类型则返回值仅一个，配置为list类型则返回值多个，和list长度一致
        :return: 根据post_action传入的值返回不同的结果，默认为空时无返回值
        :return:无
        """
        # 用例支持的关键字
        if len(caseparam) == 0 or (not isinstance(caseparam, dict)):
            raise ValueError(f"输入的caseparam无效")
        key_param = ['env', 'headers', 'query_param', 'body_param', 'form_data', 'rpc_param', 'debug', 'api_method',
                     'rpc_method', 'expect', "cluster", 'bug', 'bug_desc', 'stream', 'log_assert']
        for key in caseparam:
            if key not in key_param:
                raise ValueError(f'输入的参数有误或暂未支持，失败入参：{key}')

        # 用例关键字bug和bug_desc
        if ('bug' in caseparam) and isinstance(caseparam['bug'], bool) and caseparam['bug']:
            if 'bug_desc' in caseparam:
                pytest.skip(f"跳过原因：本用例存在问题({caseparam['bug_desc']})，暂时跳过")
            else:
                raise ValueError('请使用关键字\'bug_desc\'输入bug原因或问题跟进人，以免后续跟丢问题')

        # 用例关键字env
        env = Utils.get_env()
        if 'env' in caseparam:
            if caseparam['env'] == "" or (not isinstance(caseparam['env'], str)):
                raise ValueError("输入的运行环境无效")
            key_env = ['all', 'prod', 'pre', 'test']
            if caseparam['env'] not in key_env:
                raise ValueError(f"输入的运行环境有误或暂未支持，失败运行环境：{caseparam['env']}")
            if caseparam['env'] != 'all' and env != caseparam['env']:
                # 当用例env配置不是all时，若当前运行环境和测试用例配置环境不一致则跳过该用例
                pytest.skip(f"跳过原因：本用例仅在{caseparam['env']}环境下执行，当前环境是{env}")
        else:
            raise ValueError(f'请标明用例的运行环境')

        if ('rpc_param' in caseparam) or ('rpc_method' in caseparam):
            resp = Common.rpc_request(caseparam)
        else:
            resp = Common.api_request(caseparam)

        # STC智能校验
        if 'expect' in caseparam:
            if len(caseparam['expect']) == 0 or (not isinstance(caseparam['expect'], dict)):
                raise ValueError('输入的expect参数无效')
            stc_expect = Common.api_stc_param(caseparam['expect'])
            if 'stcAssertPart' in stc_expect.keys() and len(stc_expect) == 1:
                # 配置关键字'stcAssertPart'，则不进行多参和缺参校验
                Common.expect_assert(stc_expect['stcAssertPart'], resp, False)
            else:
                Common.expect_assert(stc_expect, resp, True)

        # log日志校验
        if 'log_assert' in caseparam:
            if len(caseparam['log_assert']) == 0 or (not isinstance(caseparam['log_assert'], dict)):
                raise ValueError('输入的 log_assert 参数无效')
            LogAssert(caseparam['log_assert']).log_assert()
            # log_expect = Common.api_stc_param(caseparam['log_assert'])
            # req = Common.api_stc_param(caseparam['rpc_param'])
            # amadeus_req, amadeus_id = LogAssert(req).post_grafana()
            # stc_expect = Common.api_stc_param(log_expect)
            # Common.expect_assert(stc_expect, amadeus_req, False)

        if post_action:
            if isinstance(post_action, list):
                ret_list = []
                for key in post_action:
                    assert isinstance(key, str), f"后置操作-输入的获取参数不合法"
                    split_key = key.split('.')
                    resp_param = resp
                    for i in range(len(split_key)):
                        if isinstance(resp_param, list):
                            k = int(split_key[i])
                        else:
                            k = split_key[i]
                        resp_param = resp_param[k]
                    ret_list.append(resp_param)
                return ret_list
            elif isinstance(post_action, str):
                split_key = post_action.split('.')
                resp_param = resp
                for i in range(len(split_key)):
                    if isinstance(resp_param, list):
                        k = int(split_key[i])
                    else:
                        k = split_key[i]
                    resp_param = resp_param[k]
                return resp_param
            else:
                raise ValueError(f'输入的post_action有误')

    @staticmethod
    def api_stc_param(param):
        if 'stc-pre' in param.keys() and 'stc-prod' in param.keys():
            if len(param) == 2:
                env = Utils.get_env()
                if env == 'pre':
                    stc_param = param['stc-pre']
                else:
                    stc_param = param['stc-prod']
            else:
                raise ValueError('stc-pre/prod关键词输入不符合规范')
        else:
            stc_param = param
        return stc_param

    @staticmethod
    def api_invoke(psm_method_name, refresh_data=None, debug=False, form_flag=False, stream=None):
        """
        使用场景：接口测试，可设置是否打印日志，便于调试使用
        使用方法：在 testcase 中的使用方法如下：
            from Swing.utils import Utils
            from api.aweme_open_api_data import AwemeOpenApidata
            resp = Utils.api_invoke(AwemeOpenApidata().data_extern_billboard_hot_video, refresh, sys._getframe().f_code.co_name, True)
        :param psm_method_name:  测试的接口对应的方法名
        :param refresh_data: psm_method_name 的接口入参，包含了：请求体、请求头、查询参数 refresh = {"query_param": {},body_param": {},"headers": {}}
        :param debug: 是否debug模式，True打印日志，False则不打印
        :param form_flag: 是否包含表单格式的文件，True包含，False则不包含
        :param stream: 是否是流式请求 True为流式请求， False则为默认请求
        :return: resp_dict 接口响应的 dict 类型
        """
        resp = psm_method_name(refresh_data=refresh_data)
        assert resp.status_code == 200
        # 判断返回的是不是音频文件
        if resp.headers['content-type'] == 'audio/mpeg':
            # 获取音频文件
            audio_file = resp.content
            return {"size": len(audio_file)}
        # 不是音频文件 正常解析json
        restructured_content = {}
        if stream:
            content = resp.content.decode('utf-8')
            # 将字符串分割成单独的事件
            events = content.strip().split('\n\n')
            # 初始化字典来存储重组后的数据
            # 遍历每个事件，解析并重组数据

            # 单独开一个开平的逻辑：
            if 'OpenPlatform' in str(psm_method_name):
                for event in events:
                    # 分割事件类型和数据部分
                    event_type, event_data = event.split(': ', 1)
                    event_type = event_type.split(':')[-1].strip()
                    # 解析数据部分为JSON
                    try:
                        data = json.loads(event_data)
                        # 将事件数据添加到重组后的字典中
                        if event_type in restructured_content:
                            # 如果事件类型已经存在，则添加到列表中
                            if not isinstance(restructured_content[event_type], list):
                                restructured_content[event_type] = [restructured_content[event_type]]
                            restructured_content[event_type].append(data)
                        else:
                            # 如果事件类型不存在，则创建一个新的键值对
                            restructured_content[event_type] = data
                    except json.JSONDecodeError as e:
                        # 打印错误信息
                        print(f"Error parsing JSON data: {e}")
            else:
                for event in events:
                    # 分割事件类型和数据部分
                    event_type, event_data = event.split('\n', 1)
                    event_type = event_type.split(':')[-1].strip()
                    event_data = event_data.replace('data:', '')
                    # 解析数据部分为JSON
                    try:
                        data = json.loads(event_data)
                        # 将事件数据添加到重组后的字典中
                        if event_type in restructured_content:
                            # 如果事件类型已经存在，则添加到列表中
                            if not isinstance(restructured_content[event_type], list):
                                restructured_content[event_type] = [restructured_content[event_type]]
                            restructured_content[event_type].append(data)
                        else:
                            # 如果事件类型不存在，则创建一个新的键值对
                            restructured_content[event_type] = data
                    except json.JSONDecodeError as e:
                        # 打印错误信息
                        print(f"Error parsing JSON data: {e}")
        query_dict = {}
        query_dict_list = []
        query_before = resp.request.path_url.split('?')
        if len(query_before) == 2:
            query_list = query_before[1].split('&')
            for i in range(len(query_list)):
                query_dict_list += query_list[i].split("=")
            for i in range(0, len(query_dict_list), 2):
                query_dict[query_dict_list[i]] = query_dict_list[i + 1]
        if len(restructured_content) > 0:
            resp_dict = restructured_content
        else:
            resp_dict = resp.json()
            # 注意 resp 是 response 类型 ;  resp.json() 是 dict 类型
        # 默认开启debug模式
        if True:
            print("\n\n")
            print(
                "********************************************** 调试日志 **********************************************")
            print("请求的url = ", resp.request.url)
            print("请求的query参数 = ",
                  json.dumps(query_dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
            if form_flag:
                print("请求的body参数 = ", resp.request.body)
            else:
                if resp.request.body:
                    print("请求的body参数 = ",
                          json.dumps(json.loads(bytes.decode(resp.request.body)), ensure_ascii=False, sort_keys=True,
                                     indent=4, separators=(',', ': ')))
                else:
                    print("请求的body参数 = ", resp.request.body)
            print("请求的headers = ",
                  json.dumps(dict(resp.request.headers), ensure_ascii=False, sort_keys=True, indent=4,
                             separators=(',', ': ')))
            # print("响应类型 type(resp) = ", type(resp))
            try:
                trace_id = resp.headers.get('trace-id')
                print("trance_id: ", trace_id)
            except KeyError:
                print("get trace_id failed")
            print("响应状态码 resp = ", resp)
            print("响应内容 resp_dict = ",
                  json.dumps(resp_dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
            print("\n\n")

        return resp_dict

    @staticmethod
    def rpc_invoke(psm_method_name, refresh=None, debug=False):
        """
        使用场景：接口测试，可设置是否打印日志，便于调试使用。同api_invoke()函数
        :param psm_method_name:  测试的接口对应的方法名
        :param refresh: psm_method_name 的接口入参，包含了：refresh
        :param debug: 是否debug模式，True打印日志，False则不打印
        :return: resp_dict 接口响应的 dict 类型
        """
        resp, logid = psm_method_name(refresh=refresh)
        # 默认开启debug模式
        if True:
            print("\n\n")
            print(
                "********************************************** rpc调试日志 **********************************************")
            print("入参 refresh = ",
                  json.dumps(refresh, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
            print("logid = ", logid)
            print("响应内容 resp = ",
                  json.dumps(resp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))
            print(
                "********************************************** rpc调试结束 **********************************************")
            print("\n\n")
        return resp

    @staticmethod
    def expect_assert(expect, resp, flag=True, need_keys=None):
        """
        使用场景：智能引擎
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :param flag: 是否进行多参和缺参校验，True=进行多参和缺参校验，False=不进行多参和缺参校验，默认为True
        :param need_keys: 需要的返回值的key，可配置string和list类型，其中，need_keys配置为string类型则返回值仅一个，配置为list类型则返回值多个，和list长度一致
        :return:无
        """
        key_expect = expect.keys()
        key_resp = resp.keys()
        flag_more = False
        key_more = []
        flag_less = False
        key_less = []
        for key in key_expect:
            if key not in key_resp:
                flag_less = True
                key_less.append(key)
        if flag_less:
            assert False, f'返回关键字校验失败，少返回关键字：{key_less}，预期返回的关键字：{key_expect}，实际返回的关键字：{key_resp}'
        if flag:
            for key in key_resp:
                if key not in key_expect:
                    flag_more = True
                    key_more.append(key)
            if flag_more:
                assert False, f'返回关键字校验失败，多返回关键字：{key_more}，预期返回的关键字：{key_expect}，实际返回的关键字：{key_resp}'
        for key in key_expect:
            # print("---------" + key + "---------")
            if isinstance(expect[key], dict):
                # print('类型判断：dict')
                if 'stcString' in expect[key].keys() and len(expect[key]) == 1:
                    # print('校验关键字判断：stcString')
                    Common.stc_string_assert(expect[key]['stcString'], resp[key])

                elif 'stcOneOf' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcOneOf')
                    Common.stc_oneof_assert(expect[key]['stcOneOf'], resp[key], key)

                elif 'stcNumberRange' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcNumberRange')
                    Common.stc_numberrange_assert(expect[key]['stcNumberRange'], resp[key])

                elif 'stcRegExp' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcRegExp')
                    Common.stc_regexp_assert(expect[key]['stcRegExp'], resp[key])

                elif 'stc-boe' in expect[key].keys() and 'stc-prod' in expect[key].keys():
                    if len(expect[key]) == 2:
                        env = Utils.get_env()
                        if env == 'pre':
                            stc_expect = expect[key]['stc-pre']
                        else:
                            stc_expect = expect[key]['stc-prod']
                    else:
                        raise ValueError(f'stc-pre/prod关键词输入不符合规范')

                    if isinstance(stc_expect, dict):
                        Common.expect_assert(stc_expect, resp[key], flag)
                    elif isinstance(stc_expect, list):
                        if isinstance(stc_expect[0], dict):
                            for i in range(len(stc_expect)):
                                Common.expect_assert(stc_expect[i], resp[key][i], flag)
                        elif isinstance(stc_expect[0], list):
                            for i in range(len(stc_expect)):
                                Common.stc_list_assert(stc_expect[i], resp[key][i])
                        else:
                            Common.stc_list_assert(stc_expect, resp[key])

                    elif stc_expect in ['dict', 'string', 'list', 'int', 'float', 'bool']:
                        if flag and stc_expect in ['dict', 'list']:
                            raise ValueError(
                                f"默认需要进行多参和缺参校验，请输入完整返回值。也可配置'stcAssertPart'关键字进行部分参数校验")
                        Common.stc_type_assert(stc_expect, resp[key])
                    else:
                        assert stc_expect == resp[
                            key], f"参数值校验失败，预期返回值：{stc_expect}，类型：{type(stc_expect)}； 实际返回值：{resp[key]}，类型：{type(resp[key])}"

                else:
                    # print('dict类型无校验关键字')
                    assert isinstance(resp[key],
                                      dict), f"返回类型校验失败，预期返回类型：{dict}，实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                    Common.expect_assert(expect[key], resp[key], flag)

            elif isinstance(expect[key], list):
                # print('类型判断：list')
                if len(expect[key]) > len(resp[key]):
                    raise IndexError(
                        f"list类型的预期值数据长度超过返回值数据长度，预期返回值：{expect[key]}，实际返回值:{resp[key]}")
                assert isinstance(resp[key],
                                  list), f"返回类型校验失败，预期返回类型：{list}，实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"

                if not expect[key]:
                    assert resp[key] == []
                else:
                    # except = [{"assert_index": 1, "name": "aaa", "aid": "1" } ,{"key_1": "value_1"}]
                    for i in range(0, len(expect[key])):
                        if isinstance(expect[key][i], dict):
                            # print(' ===== i的值是: ', i)
                            assert isinstance(resp[key][i],
                                              dict), f"返回类型校验失败，预期返回类型：{dict}，实际返回类型：{type(resp[key][i])}，实际返回值：{key}:{resp[key][i]}"
                            if 'assert_index' in expect[key][i]:
                                assert_index = expect[key][i]['assert_index']
                                expect[key][i] = {k: v for k, v in expect[key][i].items() if k != "assert_index"}

                                # 根据assert_index处理正序和倒序索引
                                if assert_index < 0:
                                    index = len(expect[key]) + assert_index
                                else:
                                    index = assert_index
                                # 检查索引是否超出范围
                                if index < 0 or index >= len(resp[key]):
                                    raise IndexError("assert_index index out of range")

                                # print(f'The assert_index is {assert_index}')
                                # 指定校验某一个index
                                Common.expect_assert(expect[key][i], resp[key][index], False)
                                continue
                            Common.expect_assert(expect[key][i], resp[key][i], False)
                            continue

                        elif isinstance(expect[key][i], list):
                            for j in range(len(expect[key])):
                                assert isinstance(resp[key][i][j],
                                                  list), f"返回类型校验失败，预期返回类型：{list}，实际返回类型：{type(resp[key][i][j])}，实际返回值：{key}:{resp[key][i]}"
                                Common.stc_list_assert(expect[key][i][j], resp[key][i][j])

                        else:
                            Common.stc_list_assert(expect[key], resp[key])

            elif expect[key] in ['dict', 'string', 'list', 'int', 'float', 'bool']:
                # print('数据value的类型判断')
                if flag and expect[key] in ['dict', 'list']:
                    raise ValueError(
                        f"默认需要进行多参和缺参校验，请输入完整返回值。也可配置'stcAssertPart'关键字进行部分参数校验")

                if expect[key] == 'int':
                    assert type(resp[
                                    key]) == int, f"参数类型校验失败，预期类型：{int}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'float':
                    assert isinstance(resp[key],
                                      float), f"参数类型校验失败，预期类型：{float}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'string':
                    assert isinstance(resp[key],
                                      str), f"参数类型校验失败，预期类型：{str}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'list':
                    assert isinstance(resp[key],
                                      list), f"参数类型校验失败，预期类型：{list}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'dict':
                    assert isinstance(resp[key],
                                      dict), f"参数类型校验失败，预期类型：{dict}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'bool':
                    assert isinstance(resp[key],
                                      bool), f"参数类型校验失败，预期类型：{bool}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"

            else:
                # print('数据的值对比')
                if isinstance(expect[key], str):
                    # 如果是string类型 先进行正则匹配
                    # regexp_flag = re.search(expect[key], str(resp[key]))
                    # 再进行数值比对
                    if expect[key] == resp[key]:
                        f"参数值校验失败，预期返回值：{key}:{expect[key]}，类型：{type(expect[key])}； 实际返回值：{key}:{resp[key]}，类型：{type(resp[key])}"
                else:
                    assert expect[key] == resp[
                        key], f"参数值校验失败，预期返回值：{key}:{expect[key]}，类型：{type(expect[key])}； 实际返回值：{key}:{resp[key]}，类型：{type(resp[key])}"

        # 新开逻辑 for 冷茶 提取key
        if need_keys is not None:
            return Common.extract_key(resp, need_keys)

    @staticmethod
    def stc_string_assert(expect, resp):
        """
        使用场景：STC智能校验引擎-关键字stcString场景校验
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :return:无
        """
        if isinstance(expect, str):
            if len(expect) == 0:
                raise ValueError(f"字符串包含校验暂不支持输入空字符串")
            else:
                assert expect in resp, f"字符串包含校验失败，预期包含值：{expect}，实际返回值：{resp}"
        else:
            raise TypeError(f"字符串包含校验输入参数类型错误，预期输入类型：{str}，实际输入：{expect}，类型：{type(expect)}")

    @staticmethod
    def stc_oneof_assert(expect, resp, key):
        """
        使用场景：STC智能校验引擎-关键字stcOneOf场景校验
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :param key: 断言的key值
        :return:无
        """
        if not (isinstance(expect, list)):
            raise TypeError(f"枚举值校验输入参数类型错误，预期类型：{list}，实际类型：{type(expect)}")
        if len(expect) <= 0:
            raise ValueError(f"枚举值校验暂不支持输入空列表, key是：{key}")

        if isinstance(expect[0], str):
            Common.one_of(expect, resp, str, key)
        elif type(expect[0]) is int:
            Common.one_of(expect, resp, int, key)
        elif isinstance(expect[0], float):
            Common.one_of(expect, resp, float, key)
        else:
            raise ValueError(f"输入的枚举值类型有误或暂未支持， key是：{key}")

    @staticmethod
    def one_of(expect, resp, value_type, key_):
        """
        使用场景：STC智能校验引擎-关键字stcOneOf场景校验的通用方法
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :param value_type: 预期返回值类型
        :param key_:
        :return:无
        """
        for key in expect:
            if not (type(key) is value_type):
                raise TypeError(f"输入枚举值类型有误，首个枚举值类型：{value_type}，错误枚举值：{key}，错误类型：{type(key)}")
        assert type(
            resp) is value_type, f"返回类型校验失败，预期返回类型：{key_}: {value_type}，实际返回类型：{key_}: {type(resp)}"
        assert resp in expect, f"枚举值校验失败，预期枚举值：{key_}: {expect}，实际返回值：{key_}: {resp}"

    @staticmethod
    def stc_numberrange_assert(expect, resp):
        """
        使用场景：STC智能校验引擎-关键字stcNumberRange场景校验
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :return:无
        """
        if not (isinstance(expect, list)):
            raise TypeError(f"数字区间校验输入参数类型错误，预期输入类型：{list}，实际输入：{expect}，类型：{type(expect)}")
        if len(expect) != 2:
            raise ValueError(f"数字区间校验输入错误，预期输入为数值区间，如：[a,b]，实际输入：{expect}")
        if not (type(expect[0]) is int or type(expect[0]) is float):
            raise TypeError(f"数字区间校验输入错误，预期输入类型：{int}或{float}，实际输入类型：{type(expect[0])}")
        if not (type(expect[1]) is int or type(expect[1]) is float):
            raise TypeError(f"数字区间校验输入错误，预期输入类型：{int}或{float}，实际输入类型：{type(expect[1])}")
        if expect[0] >= expect[1]:
            raise ValueError(f"数字区间校验输入错误，预期输入：[a,b]，其中 a < b，实际输入：{expect}")
        assert expect[0] <= resp <= expect[1], f"数字区间校验失败，预期区间：[{expect[0]}, {expect[1]}]，实际数值：{resp}"

    @staticmethod
    def stc_regexp_assert(expect, resp):
        regexp = re.search(expect, str(resp))
        assert regexp, f"正则表达式校验失败，请检查正则表达式书写是否有误或是实际返回值不符合预期，正则表达式：{expect}，实际返回值：{resp}"

    @staticmethod
    def stc_type_assert(expect, resp):
        if expect == 'int':
            assert type(resp) is int, f"参数类型校验失败，预期类型：{int}, 实际返回类型：{type(resp)}"
        elif expect == 'float':
            assert isinstance(resp, float), f"参数类型校验失败，预期类型：{float}, 实际返回类型：{type(resp)}"
        elif expect == 'string':
            assert isinstance(resp, str), f"参数类型校验失败，预期类型：{str}, 实际返回类型：{type(resp)}"
        elif expect == 'list':
            assert isinstance(resp, list), f"参数类型校验失败，预期类型：{list}, 实际返回类型：{type(resp)}"
        elif expect == 'dict':
            assert isinstance(resp, dict), f"参数类型校验失败，预期类型：{dict}, 实际返回类型：{type(resp)}"
        elif expect == 'bool':
            assert isinstance(resp, bool), f"参数类型校验失败，预期类型：{bool}, 实际返回类型：{type(resp)}"

    @staticmethod
    def stc_list_assert(expect, resp):
        assert len(expect) == len(resp), f"list类型的值校验失败，预期返回值：{expect}, 实际返回类型：{resp}"
        expect_counter = Counter(expect)
        resp_counter = Counter(resp)
        expect_dict = dict(expect_counter)
        resp_dict = dict(resp_counter)
        assert expect_dict == resp_dict, f"list类型的值校验失败，预期返回值：{expect}, 实际返回类型：{resp}"

    @staticmethod
    def api_pre_action(pre_caseparam, need_keys=""):
        """
        使用场景：前置操作，获取用例依赖的其他接口的返回值
        :param pre_caseparam: json格式的用例参数配置
        :param need_keys: 需要的返回值的key，默认是空，可配置string和list类型，其中，need_keys配置为string类型则返回值仅一个，配置为list类型则返回值多个，和list长度一致
        :return: 根据need_keys传入的值返回不同的结果
        """
        # 用例支持的关键字
        if len(pre_caseparam) == 0 or (not isinstance(pre_caseparam, dict)):
            raise ValueError(f"输入的pre_caseparam无效")
        key_param = ['env', 'headers', 'query_param', 'body_param', 'form_data', 'rpc_param', 'debug', 'api_method',
                     'rpc_method', 'expect', "cluster", 'bug', 'bug_desc', 'stream', 'log_assert']
        for key in pre_caseparam:
            if key not in key_param:
                raise ValueError(f'输入的参数有误或暂未支持，失败入参：{key}')
            elif key == "rpc_method":
                resp = Common.rpc_request(pre_caseparam)
            elif key == "api_method":
                resp = Common.api_request(pre_caseparam)

        # 前置操作可选关键字env
        env = Utils.get_env()
        if 'env' in pre_caseparam:
            if pre_caseparam['env'] == "" or (not isinstance(pre_caseparam['env'], str)):
                raise ValueError(f"输入的运行环境无效")
            key_env = ['all', 'prod', 'pre', 'test']
            if pre_caseparam['env'] not in key_env:
                raise ValueError(f"输入的运行环境有误或暂未支持，失败运行环境：{pre_caseparam['env']}")
            if pre_caseparam['env'] != 'all' and env != pre_caseparam['env']:
                # 当前置操作env配置不是all时，若当前运行环境和前置操作配置环境不一致则跳过该前置操作
                pytest.skip(f"跳过原因：本前置操作仅在{pre_caseparam['env']}环境下执行，当前环境是{env}")

        if 'timeout' in pre_caseparam:
            if not isinstance(pre_caseparam['timeout'], int):
                raise ValueError(f'输入的timeout参数无效')
            time.sleep(pre_caseparam['timeout'])

        if need_keys:
            if isinstance(need_keys, list):
                ret_list = []
                for key in need_keys:
                    assert isinstance(key, str), f"前置操作-输入的获取参数不合法"
                    split_key = key.split('.')
                    resp_param = resp
                    for i in range(len(split_key)):
                        if isinstance(resp_param, list):
                            k = int(split_key[i])
                        else:
                            k = split_key[i]
                        resp_param = resp_param[k]
                    ret_list.append(resp_param)
                return ret_list
            elif isinstance(need_keys, str):
                split_key = need_keys.split('.')
                resp_param = resp
                for i in range(len(split_key)):
                    if isinstance(resp_param, list):
                        k = int(split_key[i])
                    else:
                        k = split_key[i]
                    resp_param = resp_param[k]
                return resp_param
            else:
                raise ValueError(f'输入的need_keys有误')
        else:
            return resp

    @staticmethod
    def extract_key(resp, need_keys):
        """
        使用场景：前置操作，获取用例依赖的其他接口的返回值
        :param resp: json格式的用例参数配置
        :param need_keys: 需要的返回值的key，可配置string和list类型，其中，need_keys配置为string类型则返回值仅一个，配置为list类型则返回值多个，和list长度一致
        :return: 根据need_keys传入的值返回不同的结果
        """
        if isinstance(need_keys, list):
            ret_list = []
            for key in need_keys:
                assert isinstance(key, str), f"前置操作-输入的获取参数不合法"
                split_key = key.split('.')
                resp_param = resp
                for i in range(len(split_key)):
                    if isinstance(resp_param, list):
                        k = int(split_key[i])
                    else:
                        k = split_key[i]
                    resp_param = resp_param[k]
                ret_list.append(resp_param)
            return ret_list
        elif isinstance(need_keys, str):
            split_key = need_keys.split('.')
            resp_param = resp
            for i in range(len(split_key)):
                if isinstance(resp_param, list):
                    k = int(split_key[i])
                else:
                    k = split_key[i]
                resp_param = resp_param[k]
            return resp_param
        else:
            raise ValueError(f'输入的need_keys有误')

    @staticmethod
    def api_post_action(post_caseparam):
        """
        使用场景：后置操作
        :param post_caseparam: json格式的用例参数配置
        :return: 无
        """
        # 用例支持的关键字
        if len(post_caseparam) == 0 or (not isinstance(post_caseparam, dict)):
            raise ValueError(f"输入的pre_caseparam无效")
        key_param = ['env', 'headers', 'query_param', 'body_param', 'form_data', 'rpc_param', 'debug', 'api_method',
                     'rpc_method', 'expect', "cluster", 'bug', 'bug_desc', 'stream', 'log_assert']
        for key in post_caseparam:
            if key not in key_param:
                raise ValueError(f'输入的参数有误或暂未支持，失败入参：{key}')

        if 'timeout' in post_caseparam:
            if not isinstance(post_caseparam['timeout'], int):
                raise ValueError(f'输入的timeout参数无效')
            time.sleep(post_caseparam['timeout'])

        resp = Common.api_request(post_caseparam)

        if 'expect' in post_caseparam:
            if len(post_caseparam['expect']) == 0 or (not isinstance(post_caseparam['expect'], dict)):
                raise ValueError(f'输入的expect参数无效')
            Common.expect_assert(post_caseparam['expect'], resp, False)
        else:
            raise ValueError(f'请输入校验内容')

    @staticmethod
    def is_subset(dict_a, dict_b):
        """
        判断dictA是否是dictB的子集。
        """
        for key, _ in dict_a.items():
            # 如果键不存在于dictB中，或者键对应的值不相等，则返回False
            if key not in dict_b:
                return False
        # 如果所有键值对都匹配，则返回True
        return True

    @staticmethod
    def expect_assert_re(expect, resp, flag=True, need_keys=None):
        """
        使用场景：智能引擎--所有的string都会做正则校验
        :param expect: 预期返回值
        :param resp: 接口实际返回值
        :param flag: 是否进行多参和缺参校验，True=进行多参和缺参校验，False=不进行多参和缺参校验，默认为True
        :param need_keys: 需要的返回值的key，可配置string和list类型，其中，need_keys配置为string类型则返回值仅一个，配置为list类型则返回值多个，和list长度一致
        :return:无
        """
        key_expect = expect.keys()
        key_resp = resp.keys()
        flag_more = False
        key_more = []
        flag_less = False
        key_less = []
        for key in key_expect:
            if key not in key_resp:
                flag_less = True
                key_less.append(key)
        if flag_less:
            assert False, f'返回关键字校验失败，少返回关键字：{key_less}，预期返回的关键字：{key_expect}，实际返回的关键字：{key_resp}'
        if flag:
            for key in key_resp:
                if key not in key_expect:
                    flag_more = True
                    key_more.append(key)
            if flag_more:
                assert False, f'返回关键字校验失败，多返回关键字：{key_more}，预期返回的关键字：{key_expect}，实际返回的关键字：{key_resp}'
        for key in key_expect:
            # print("---------" + key + "---------")
            if isinstance(expect[key], dict):
                # print('类型判断：dict')
                if 'stcString' in expect[key].keys() and len(expect[key]) == 1:
                    # print('校验关键字判断：stcString')
                    Common.stc_string_assert(expect[key]['stcString'], resp[key])

                elif 'stcOneOf' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcOneOf')
                    Common.stc_oneof_assert(expect[key]['stcOneOf'], resp[key], key)

                elif 'stcNumberRange' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcNumberRange')
                    Common.stc_numberrange_assert(expect[key]['stcNumberRange'], resp[key])

                elif 'stcRegExp' in expect[key].keys() and len(expect[key]) == 1:
                    # print('检验关键字判断：stcRegExp')
                    Common.stc_regexp_assert(expect[key]['stcRegExp'], resp[key])

                elif 'stc-boe' in expect[key].keys() and 'stc-prod' in expect[key].keys():
                    if len(expect[key]) == 2:
                        env = Utils.get_env()
                        if env == 'pre':
                            stc_expect = expect[key]['stc-pre']
                        else:
                            stc_expect = expect[key]['stc-prod']
                    else:
                        raise ValueError(f'stc-pre/prod关键词输入不符合规范')

                    if isinstance(stc_expect, dict):
                        Common.expect_assert(stc_expect, resp[key], flag)
                    elif isinstance(stc_expect, list):
                        if isinstance(stc_expect[0], dict):
                            for i in range(len(stc_expect)):
                                Common.expect_assert(stc_expect[i], resp[key][i], flag)
                        elif isinstance(stc_expect[0], list):
                            for i in range(len(stc_expect)):
                                Common.stc_list_assert(stc_expect[i], resp[key][i])
                        else:
                            Common.stc_list_assert(stc_expect, resp[key])

                    elif stc_expect in ['dict', 'string', 'list', 'int', 'float', 'bool']:
                        if flag and stc_expect in ['dict', 'list']:
                            raise ValueError(
                                f"默认需要进行多参和缺参校验，请输入完整返回值。也可配置'stcAssertPart'关键字进行部分参数校验")
                        Common.stc_type_assert(stc_expect, resp[key])
                    else:
                        assert stc_expect == resp[
                            key], f"参数值校验失败，预期返回值：{stc_expect}，类型：{type(stc_expect)}； 实际返回值：{resp[key]}，类型：{type(resp[key])}"

                else:
                    # print('dict类型无校验关键字')
                    assert isinstance(resp[key],
                                      dict), f"返回类型校验失败，预期返回类型：{dict}，实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                    Common.expect_assert(expect[key], resp[key], flag)

            elif isinstance(expect[key], list):
                # print('类型判断：list')
                if len(expect[key]) > len(resp[key]):
                    raise IndexError(
                        f"list类型的预期值数据长度超过返回值数据长度，预期返回值：{expect[key]}，实际返回值:{resp[key]}")
                assert isinstance(resp[key],
                                  list), f"返回类型校验失败，预期返回类型：{list}，实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"

                if not expect[key]:
                    assert resp[key] == []
                else:
                    count = 0
                    for i in range(0, len(expect[key])):
                        if 'placeholder' in expect[key][i] and isinstance(expect[key][i], dict):
                            count += expect[key][i]['placeholder']
                            i = count

                        elif isinstance(expect[key][i], dict):
                            assert isinstance(resp[key][i],
                                              dict), f"返回类型校验失败，预期返回类型：{dict}，实际返回类型：{type(resp[key][i])}，实际返回值：{key}:{resp[key][i]}"
                            if Common.is_subset(expect[key][i + count], resp[key][i + count]):
                                Common.expect_assert(expect[key][i + count], resp[key][i + count], False)

                        elif isinstance(expect[key][i], list):
                            for i in range(len(expect[key])):
                                assert isinstance(resp[key][i],
                                                  list), f"返回类型校验失败，预期返回类型：{list}，实际返回类型：{type(resp[key][i])}，实际返回值：{key}:{resp[key][i]}"
                                Common.stc_list_assert(expect[key][i], resp[key][i])

                        else:
                            Common.stc_list_assert(expect[key], resp[key])

            elif expect[key] in ['dict', 'string', 'list', 'int', 'float', 'bool']:
                # print('数据value的类型判断')
                if flag and expect[key] in ['dict', 'list']:
                    raise ValueError(
                        f"默认需要进行多参和缺参校验，请输入完整返回值。也可配置'stcAssertPart'关键字进行部分参数校验")

                if expect[key] == 'int':
                    assert type(resp[
                                    key]) == int, f"参数类型校验失败，预期类型：{int}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'float':
                    assert isinstance(resp[key],
                                      float), f"参数类型校验失败，预期类型：{float}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'string':
                    assert isinstance(resp[key],
                                      str), f"参数类型校验失败，预期类型：{str}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'list':
                    assert isinstance(resp[key],
                                      list), f"参数类型校验失败，预期类型：{list}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'dict':
                    assert isinstance(resp[key],
                                      dict), f"参数类型校验失败，预期类型：{dict}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"
                elif expect[key] == 'bool':
                    assert isinstance(resp[key],
                                      bool), f"参数类型校验失败，预期类型：{bool}, 实际返回类型：{type(resp[key])}，实际返回值：{key}:{resp[key]}"

            else:
                # print('数据的值对比')
                if isinstance(expect[key], str):
                    # 如果是string类型 先进行正则匹配
                    assert re.search(expect[key], str(resp[key])),  f"参数值校验失败，预期返回值：{key}:{expect[key]}，类型：{type(expect[key])}； 实际返回值：{key}:{resp[key]}，类型：{type(resp[key])}"
                else:
                    assert expect[key] == resp[
                        key], f"参数值校验失败，预期返回值：{key}:{expect[key]}，类型：{type(expect[key])}； 实际返回值：{key}:{resp[key]}，类型：{type(resp[key])}"

        # 新开逻辑 for 冷茶 提取key
        if need_keys is not None:
            return Common.extract_key(resp, need_keys)


if __name__ == '__main__':
    resp = {'key_1': 'value_1', 'key_2': 'value_2'}
    expect_resp = {'key_1': 'value_1', 'key_2': 'value_2'}
    print(Common.expect_assert(resp, expect_resp, False, need_keys='key_1'))
