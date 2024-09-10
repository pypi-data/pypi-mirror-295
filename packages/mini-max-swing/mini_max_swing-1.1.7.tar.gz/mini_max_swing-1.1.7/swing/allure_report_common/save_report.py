"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/3 下午2:17
@Author: xingyun
"""
import zipfile
import os
from datetime import datetime

import requests

from swing.allure_report_common.util import Util
from swing.rpc_generator.plugins.log.logger import logger
from swing.common.tos import Tos
from swing.common.mysql_op import MysqlOp

bucket_path = 'qa-tool-1315599187'
swing_report_path = 'swingReport/'


class SaveReport(object):
    def __init__(self, job_id, operator, psm, status, env, env_label, stage_name, task_id):
        self.job_id = job_id
        self.operator = operator
        self.psm = psm
        self.stage_name = stage_name
        self.task_id = task_id
        self.create_time = str(datetime.now())
        self.status = status
        self.env = env
        self.env_label = env_label

    def save_report(self, report_path=None) -> bool:
        """
        :param self:
        :param report_path:
        """
        # 先压缩
        # 报告路径
        if report_path is None:
            report_path = Util.get_report_path()
        logger.info('get report_path: %s' % report_path)
        # 压缩文件的命名： swing_report_20240623_job_id.zip
        zip_file = 'swing_report' + '_' + Util.time_formatted() + '_' + str(self.job_id) + '.zip'
        # 创建一个ZipFile对象
        logger.info('save zip file: %s' % zip_file)
        # 创建ZIP文件
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            for root, dirs, files in os.walk(report_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), report_path))

        logger.info('save zip file successfully')
        # 上传tos
        # bucket_path: qa-tool-1315599187/
        # tos的path路径：swingReport/20240623/swing_report_20240623_job_id.zip
        file_key = swing_report_path + Util.time_formatted() + '/' + zip_file
        logger.info('tos key: %s' % file_key)
        local_path = os.getcwd() + '/' + zip_file
        tos = Tos()
        logger.info('put report to tos, local_path:\n %s' % local_path)
        tos.put_object_to_bucket(bucket_path, local_path, file_key)
        # 判断是否上传成功， 上传失败 重新上传
        if not tos.exists_object(bucket_path, file_key):
            logger.error('save tos file failed, retry......')
            tos.put_object_to_bucket(bucket_path, local_path, file_key)
            logger.info('retry tos end')
            
        # 上传数据库
        try:
            logger.info('======start insert data into database')
            report_tos_key = bucket_path + file_key
            insert_sql = ('insert into swing_report (operator, psm, stage_name, task_id, report_tos_key, status, '
                          'create_time, env, job_id, env_label) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            MysqlOp().connect(insert_sql, data=(
                self.operator, self.psm, self.stage_name, self.task_id, report_tos_key, self.status, self.create_time,
                self.env, self.job_id, self.env_label),
                              op='insert')
        except Exception as e:
            logger.error(e)
        return

    def get_server(self):
        fast_project_url = f'http://swing.xaminim.com/run/allure/{self.job_id}'
        resp = requests.get(fast_project_url)
        logger.info(resp)
        if resp.ok:
            print('Status Code:', resp.status_code)
            print('Response Content:', resp.text)
            return resp.json()['server']

        # 请求失败，打印错误信息
        print('Error:', resp.status_code, resp.reason)


if __name__ == '__main__':
    SaveReport(987654321, 'xingyun', 'open_platform', 'success', 'prod', 'prod', 'kaiping', '111111111111').save_report()
    # SaveReport(123456, 'xingyun', 'open_platform', True, 'prod').get_server()

