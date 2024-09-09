"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/4 下午5:48
@Author: xingyun
"""

import pymysql

from datetime import datetime
from rpc_generator.plugins.log.logger import logger


class MysqlOp(object):
    def __init__(self):
        self.password = 'ngo0nZYnPvpoke7P'
        self.host = '10.11.24.40'
        self.database = 'qa_tools'
        self.user = 'qa_test'
        self.port = 3306
        self.table = 'pingan_un_bank_info'

    def connect(self, sql_, data=None, op=None):
        # 连接到MySQL数据库
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               password=self.password,
                               db=self.database,
                               port=self.port)

        # 创建Cursor对象
        try:
            with conn.cursor() as cursor:
                if op == 'insert':
                    cursor.execute(sql_, data)
                    conn.commit()
                    # 插入成功后，可以获取插入数据的ID（如果表有自增主键）
                    last_id = cursor.lastrowid
                    logger.info(f"Last inserted record ID is {last_id}")
                elif op == 'select':
                    cursor.execute(sql_, data)
                    # 获取查询结果
                    results = cursor.fetchall()
                    # 打印结果
                    for row in results:
                        logger.info(row)
                elif op == 'delete':
                    cursor.execute(sql_, data)

        except pymysql.MySQLError as e:
            # 如果发生错误，打印错误信息
            logger.info(f"Error: {e}")
        finally:
            # 关闭Cursor和Connection
            conn.close()


if __name__ == '__main__':
    group_id = '112233445566'
    bank_account_no = 'test_1234'
    card_num = 'test_card_num'
    redis_key = 'cred_group_id_data'
    ping_an_resp = 'xxx'
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    mysql_op = MysqlOp()
    sql_ = 'insert into pingan_un_bank_info (group_id, bank_account_no, card_num, redis_key, pingan_url_resp, creat_time, delete_time) values (%s, %s, %s, %s, %s, %s, %s)'
    mysql_op.connect(sql_=sql_, data=(group_id, bank_account_no, card_num, redis_key, ping_an_resp, time_stamp, time_stamp), op='insert')

    # operator_ = 'xingyun'
    # psm_ = 'open_platform'
    # task_name_ = '开放平台线上环境巡检'
    # task_id_ = '123456xxx'
    # job_id = '13579098'
    # report_url_ = ''
    # report_tos_key_ = 'qa-tool-1315599187/swingReport/20240604/swing_report_20240604_123456.zip'
    # status_ = True
    # create_time_ = str(datetime.now())
    # env_ = 'prod'
    # sql = 'insert into swing_report (operator, psm, task_name, task_id, report_url, report_tos_key, status, create_time, env, job_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    # MysqlOp().connect(sql, data=(operator_, psm_, task_name_, task_id_, report_url_, report_tos_key_, status_, create_time_, env_, job_id), op='insert')
    # sql = 'select * from swing_report where task_id = %s'
    # mys = MysqlOp()
    # mys.connect(sql_=sql, data=(task_id_,), op='select')
