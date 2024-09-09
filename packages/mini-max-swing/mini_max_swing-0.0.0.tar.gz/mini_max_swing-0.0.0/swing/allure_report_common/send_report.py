"""
coding:utf-8
@Software: PyCharm
@Time: 2024/5/31 下午2:56
@Author: xingyun
"""
# encoding=utf-8
import json
import os

import requests

import hashlib
import base64
import hmac
import time
from allure_report_common.get_report_message import GetReportMessage
from rpc_generator.plugins.log.logger import logger
from rpc_generator.utils.utils import Utils
from allure_report_common.util import Util


class SendReport(object):
    def __init__(self):
        self.env = Utils.get_conf('common', 'env')
        # 获取当前的UTC时间
        self.timestamp = int(time.time())
        report_title_key = self.env + '_report_title'
        report_scene_key = self.env + '_report_scene'
        self.title = Utils.get_conf('report_message', report_title_key)
        self.scene = Utils.get_conf('report_message', report_scene_key)
        # todo 从上下文参数中获取信息：operator job_id psm env env_label
        # 默认值
        self.job_id = Util.time_formatted_shanghai()
        self.operator = 'xingyun'
        self.psm = 'open_platform'
        self.env = 'prod'
        self.env_label = 'prod'
        self.stage_name = '线上环境回归'
        # 尝试从环境变量中获取 bedrock 相关的值
        if 'bedrock' in os.environ:
            bedrock_value = os.environ['bedrock']
            try:
                bedrock_value_dict = json.loads(bedrock_value)
                self.job_id = bedrock_value_dict.get('jobId', self.job_id)
                self.operator = bedrock_value_dict.get('operator', self.operator)
                self.psm = bedrock_value_dict.get('psm', self.psm)
                self.env = bedrock_value_dict.get('env', self.env)
                self.env_label = bedrock_value_dict.get('env_label', self.env_label)
                self.stage_name = bedrock_value_dict.get('stage_name', self.stage_name)
                self.cluster = bedrock_value_dict.get('cluster', '')
                self.project = bedrock_value_dict.get('project', '')
                # cicd消息通知模板更改 title == “cicd tns-content-content-risk test任务报告”
                self.title = f'CICD {self.project.upper()} 业务线 任务报告'
            except json.JSONDecodeError:
                logger.info('Failed to parse bedrock JSON value')

        # 打印获取到的值
        logger.info(f'=================Job ID: {self.job_id}')
        logger.info(f'=================Operator: {self.operator}')
        logger.info(f'=================PSM: {self.psm}')
        logger.info(f'=================Environment: {self.env}')
        logger.info(f'=================Environment Label: {self.env_label}')
        logger.info(f'=================Stage Name: {self.stage_name}')
        logger.info(f'=================timestamp: {self.timestamp}')

    def gen_sign(self, report_secret):
        # 拼接timestamp和secret
        logger.info('===== gen_sign timestamp is ====')
        logger.info(self.timestamp)
        string_to_sign = '{}\n{}'.format(self.timestamp, report_secret)
        hmac_code = hmac.new(string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_report(self):
        logger.info('======= start get report =======')
        report_msg, run_status = self.get_content_msg()
        report_url = Utils.get_conf('report_message', 'success_report_url')
        report_secret = Utils.get_conf('report_message', 'success_report_secret')
        logger.info(f'================run status: {run_status}')
        # 成功的话 发送小群，失败的话 发送报警群
        if not run_status:
            report_url = Utils.get_conf('report_message', 'fail_report_url')
            report_secret = Utils.get_conf('report_message', 'fail_report_secret')

        logger.info(f'================report_url=========\n{report_url}')
        try:
            sign = self.gen_sign(report_secret)
            report_msg['timestamp'] = self.timestamp
            logger.info(f'======== send_report timestamp: {report_msg["timestamp"]}')
            logger.info(f'======== send_report sign: {sign}')
            report_msg['sign'] = sign
            res = requests.post(report_url, json=report_msg, verify=False)
            logger.info(f'=======res is:  {res.text}')
            logger.info(res.content)

            assert res.status_code == 200
            assert res.json()['StatusCode'] == 0
            return True
        except Exception as e:
            raise Exception(e)

    def get_content_msg(self):
        # 先获取运行信息
        report_message = GetReportMessage(self.job_id, self.operator, self.psm, self.env, self.env_label,
                                          self.stage_name).get_result_message()
        content = '**' + self.scene + ', 测试完成' + '**\n'
        run_status = True
        try:
            # 没有失败的case
            if report_message['result_message']['fail_count'] == 0 and report_message['result_message']['broken_count'] == 0:
                success_count = '通过 ({case_pass}/{case_count})      '.format(
                    case_pass=report_message['result_message']['success_count'],
                    case_count=report_message['result_message']['total_count'])
                content += success_count
                skip_count = '跳过({case_pass}/{case_count})      '.format(
                    case_pass=report_message['result_message']['skipped_count'],
                    case_count=report_message['result_message']['total_count'])
                content += skip_count
                content += '\n'
                report_url = '测试报告：[点击跳转测试报告]($urlVal)'
                content += report_url
                if 'bedrock' in os.environ:
                    content += '\n'
                    psm = f'运行的psm：{self.psm}'
                    content += psm
                    content += '\n'
                    cluster = f'运行的环境：{self.cluster}'
                    content += cluster
                    content += '\n'
                    bedrock_url = f'bedrock地址：https://bedrock.xaminim.com/#/projects/{self.project}/apps/{self.psm}'
                    content += bedrock_url
            else:
                run_status = False
                try:
                    fail_count = '未通过 ({case_pass}/{case_count})        '.format(
                        case_pass=report_message['result_message']['fail_count'],
                        case_count=report_message['result_message']['total_count'])
                    success_count = '通过 ({case_pass}/{case_count})      '.format(
                        case_pass=report_message['result_message']['success_count'],
                        case_count=report_message['result_message']['total_count'])
                    skip_count = '跳过({case_pass}/{case_count})      '.format(
                        case_pass=report_message['result_message']['skipped_count'],
                        case_count=report_message['result_message']['total_count'])
                    broken_count = '中断 ({case_pass}/{case_count})      '.format(
                        case_pass=report_message['result_message']['broken_count'],
                        case_count=report_message['result_message']['total_count'])
                    content += success_count
                    content += skip_count
                    content += fail_count
                    content += broken_count
                    if report_message['result_message']['fail_count'] != 0:
                        for i in range(0, len(report_message['failure_message'])):
                            message = report_message['failure_message'][i]
                            content_title = '\n========第 ' + str(i + 1) + ' 个失败的case信息 ========\n'
                            content += content_title
                            fail_message = '    失败的path：' + message['fail_case_path'] + '\n' + '    失败描述：' + \
                                           message[
                                               'fail_case_desc'] + '\n' + '    失败原因：' + message[
                                               'fail_case_status_message'] + '\n' + '    trace_id：' + \
                                           message['fail_case_trace_id']
                            content += fail_message
                    if report_message['result_message']['broken_count'] != 0:
                        for i in range(0, len(report_message['broken_message'])):
                            message = report_message['broken_message'][i]
                            content_title = '\n========第 ' + str(i + 1) + ' 个中断的case信息 ========\n'
                            content += content_title
                            fail_message = '    失败的path：' + message['fail_case_path'] + '\n' + '    失败描述：' + \
                                           message[
                                               'fail_case_desc'] + '\n' + '    中断原因：' + message[
                                               'fail_case_status_message'] + '\n'
                            content += fail_message
                except Exception as e:
                    logger.info(e)
                content += '\n'
                report_url = '测试报告：[点击跳转测试报告]($urlVal)'
                content += report_url
                if 'bedrock' in os.environ:
                    content += '\n'
                    bedrock_url = f'bedrock运行地址：https://bedrock.xaminim.com/#/projects/{self.project}/apps/{self.psm}'
                    content += bedrock_url
                content += '\n'
                content += "<at id=all></at>"
            msg = {
                "msg_type": "interactive",
                "card": {
                    "header": {
                        "template": "blue",
                        "title": {
                            "content": self.title,
                            "tag": "plain_text"
                        }
                    },
                    "elements": [{
                        "tag": "div",
                        "text": {
                            "content": content,
                            "tag": "lark_md",
                            "href": {
                                "urlVal": {
                                    "url": F"http://{report_message['report_url']}",
                                }
                            }
                        }
                    }
                    ]
                }
            }
            return msg, run_status
        except Exception as e:
            raise Exception(e)


def send_report_test():
    timestamp = SendReport().timestamp
    print('init timestamp is ====')
    print(timestamp)
    report_msg = {
        "timestamp": timestamp,
        "sign": "",
        "msg_type": "text",
        "content": {
            "text": "request example"
        }
    }
    report_url = Utils.get_conf('report_message', 'fail_report_url')
    report_secret = Utils.get_conf('report_message', 'fail_report_secret')
    sign = SendReport().gen_sign(report_secret)

    report_msg['sign'] = sign
    print('=======report_msg is =======')
    print(report_msg)
    resp = requests.post(report_url, json=report_msg, verify=False)
    print('=====resp is =======')
    print(resp)

    assert resp.status_code == 200
    assert resp.json()['StatusCode'] == 0


if __name__ == '__main__':
    # send_report_test()
    SendReport().send_report()
