"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/25 15:31
@Author: xingyun
"""
import traceback
from functools import wraps
import logging


def get_logger():
    """        
    框架中底层所使用的方法，业务一般不建议使用，用于定义logger，业务如想使用，可以使用logger = get_logger() logger.info()
    :return:
    """
    logger = logging.getLogger('prekLogger')
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    format_str = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(message)s"
    date_format_str = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format_str)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def log_decorate(func):
    """
    装饰器，业务可以直接使用，主要是打印当前运行了什么方法
    :param func: 函数名称
    :return:
    """
    @wraps(func)
    def log(*args, **kwargs):
        try:
            print("当前运行方法: ", func.__name__)
            return func(*args, **kwargs)
        except Exception as e:
            get_logger().error(f"{func.__name__} is error, logId: {e.args},  errMsg is: {traceback.format_exc()}")

    return log
