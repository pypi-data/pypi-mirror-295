"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/4 下午2:43
@Author: xingyun
"""

import os
import pytz

from datetime import datetime, timedelta


class Util(object):
    def __init__(self):
        pass

    @staticmethod
    def get_report_path() -> str:
        if 'lib' in os.getcwd():
            root_path = os.path.dirname(os.path.abspath(os.getcwd()))
        # 命令行处理
        else:
            root_path = os.getcwd()
        report_path = root_path + '/report/'

        return report_path

    @staticmethod
    def time_formatted() -> str:
        # 获取当前日期和时间
        current_date = datetime.now()
        # 获取上海时区
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        # 将当前日期和时间转换为上海时区
        shanghai_time = current_date.astimezone(shanghai_tz)
        # 格式化日期为 YYYYMMDD 格式
        formatted_date = shanghai_time.strftime('%Y%m%d')
        return formatted_date

    @staticmethod
    def time_formatted_shanghai() -> str:
        # 获取当前日期和时间
        current_date = datetime.now()
        # 获取上海时区
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        # 将当前日期和时间转换为上海时区
        shanghai_time = current_date.astimezone(shanghai_tz)
        # 格式化日期为 YYYYMMDD 格式
        formatted_date = shanghai_time.strftime('%Y%m%d%H%M%S')
        return formatted_date


if __name__ == '__main__':
    # 获取当前的UTC时间
    utc_now = datetime.utcnow()
    # 将UTC时间转换为北京时间（UTC+8）
    beijing_now = utc_now + timedelta(hours=8)
    # 获取北京时间的时间戳
    beijing_timestamp = int(beijing_now.timestamp())
    print(beijing_timestamp)


