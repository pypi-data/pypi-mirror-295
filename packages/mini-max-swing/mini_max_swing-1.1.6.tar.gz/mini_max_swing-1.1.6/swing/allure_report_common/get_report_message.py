"""
coding:utf-8
@Software: PyCharm
@Time: 2024/5/31 下午12:36
@Author: xingyun
"""
import json
import os.path
import re
import time
from swing.rpc_generator.plugins.log.logger import logger
from swing.allure_report_common.save_report import SaveReport


class GetReportMessage:
    def __init__(self, job_id, operator, psm, env, env_label, stage_name):
        if 'lib' in os.getcwd():
            root_path = os.path.dirname(os.path.abspath(os.getcwd()))
        # 命令行处理
        else:
            root_path = os.getcwd()
        self.job_id = job_id
        self.report_path = root_path + '/allure/report/'
        self.fail_case_path_root = root_path + '/allure/report/data'
        self.operator = operator
        self.psm = psm
        self.stage_name = stage_name
        # 无效字段
        self.task_id = '135678901765433324'
        self.env = env
        self.env_label = env_label

    def get_result_message(self):
        """
        :description: 获取运行结果信息
        :param
        :return: report_message{
            'result_message': {
                success_count: int
                failure_count: int
                total_count: int
                skipped_count: int
                success_rate: float
            }
            'failure_message': [
                {
                    fail_case_path: sting
                    fail_case_desc: string
                    fail_case_trace_id: string
                },
                {
                    fail_case_path: sting
                    fail_case_desc: string
                    fail_case_trace_id: string
                }
            ]
            'report_url': report_url
        }
        """
        run_status = 'success'
        result_massage = {}
        report_message = {}
        logger.info(f'==========report_path===========\n{self.report_path}')
        # 判断路径是否存在
        for sec in range(0, 1000):
            time.sleep(1)
            logger.info('=========wait for report generator =========')
            if os.path.exists(self.report_path):
                break
        # 获取case的运行结果
        summary_path = self.report_path + 'widgets/summary.json'
        try:
            with open(summary_path, 'r') as f:
                summary = json.load(f)
                result_massage['success_count'] = summary['statistic']['passed']
                result_massage['fail_count'] = summary['statistic']['failed']
                result_massage['total_count'] = summary['statistic']['total']
                result_massage['skipped_count'] = summary['statistic']['skipped']
                result_massage['broken_count'] = summary['statistic']['broken']
                result_massage['success_rate'] = result_massage['success_count'] / result_massage['total_count'] * 100
                report_message['result_message'] = result_massage

        except Exception as e:
            print(e)
        logger.info(f'=========get report_result success=====\n{self.report_path}')
        logger.info(f'==========report message=========\n{report_message}')        # 有错误的case 获取错误的case
        # 获取失败的case详情
        if result_massage['fail_count'] != 0:
            run_status = 'failure'
            duration_path = self.report_path + 'widgets/duration.json'
            fail_uid_list = []
            try:
                # 获取对应的错误信息的UID
                with open(duration_path, 'r') as f:
                    duration = json.load(f)
                    # print(duration)
                    for i in range(0, len(duration)):
                        if duration[i]['status'] == 'failed':
                            fail_uid_list.append(duration[i]['uid'])
                    failure_message = self.get_fail_message(fail_uid_list)
                    logger.info(f'failure_message is ======:\n{failure_message}')
                    report_message['failure_message'] = failure_message
            except Exception as e:
                logger.info(e)

        # 获取broken的case详情
        if result_massage['broken_count'] != 0:
            duration_path = self.report_path + 'widgets/duration.json'
            fail_uid_list = []
            try:
                # 获取对应的错误信息的UID
                with open(duration_path, 'r') as f:
                    duration = json.load(f)
                    # print(duration)
                    for i in range(0, len(duration)):
                        if duration[i]['status'] == 'broken':
                            fail_uid_list.append(duration[i]['uid'])
                    failure_message = self.get_fail_message(fail_uid_list)
                    logger.info(f'failure_message is ======:\n{failure_message}')
                    report_message['broken_message'] = failure_message
            except Exception as e:
                logger.info(e)

        # 保存数据和启动allure
        report_url = self.save_report_message(run_status)
        report_message['report_url'] = str(report_url)
        logger.info(f'==========report_message==========\n{report_message}')
        logger.info(report_message)
        return report_message

    def get_fail_message(self, fail_uid_list):
        """
        获取运行中错误的信息
        :param fail_uid_list: 失败的uid_list
        :return:
        """
        failure_message = []
        for fail_uid in fail_uid_list:
            fail_message_of_one = {}
            fail_case_path = self.fail_case_path_root + '/test-cases/' + fail_uid + '.json'
            try:
                with open(fail_case_path, 'r') as f:
                    fail_case = json.load(f)
                    if fail_case['status'] == 'failed' or fail_case['status'] == 'broken':
                        fail_message_of_one['fail_case_path'] = fail_case['name']
                        fail_message_of_one['fail_case_desc'] = fail_case.get('description', 'None ').strip()
                        fail_message_of_one['fail_case_status_message'] = fail_case['statusMessage'].replace('<',
                                                                                                             '').replace(
                            '>', '')
                        # 获取trance_id
                        attachments_path = self.fail_case_path_root + '/attachments/' + \
                                           fail_case['testStage']['attachments'][0]['source']
                        # 获取错误信息详情
                        try:
                            with open(attachments_path, 'r', encoding='utf-8') as af:
                                # 读取所有行到一个列表中
                                lines = af.readlines()
                                # 打印每一行
                                re.compile(r'"trance_id":\s*"([^"]*)"')
                                for line in lines:
                                    # 使用正则表达式匹配并提取trace_id的值
                                    if 'trance_id' in line:
                                        trace_id_value = line.split(': ')[1]
                                        print("trace_id_value:", trace_id_value)
                                        fail_message_of_one['fail_case_trace_id'] = trace_id_value
                                        break

                                # 增加trace_id校验，没有的话给一个默认值
                                if 'fail_case_trace_id' not in fail_message_of_one:
                                    fail_message_of_one['fail_case_trace_id'] = ''

                                    # 使用strip()移除行尾的换行符
                        except Exception as e:
                            print(e)
                failure_message.append(fail_message_of_one)
            except Exception as e:
                print(e)
        return failure_message

    def save_report_message(self, status: str) -> str:
        logger.info('======= save report to tos&mysql =======')
        save_message = SaveReport(self.job_id, self.operator, self.psm, status, self.env, self.env_label,
                                  self.stage_name, self.task_id)
        # 失败不影响后面的消息发送
        try:
            # step1 保存详细信息至数据库
            save_message.save_report(self.report_path)
            # step2 启动allure 获取ip+port
            logger.info('======= start run allure =======')
            report_url = save_message.get_server()
            return report_url
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    test = GetReportMessage('11', '11', '11', '11', '1', '1').get_result_message()
    print('\n')
    print(test)
