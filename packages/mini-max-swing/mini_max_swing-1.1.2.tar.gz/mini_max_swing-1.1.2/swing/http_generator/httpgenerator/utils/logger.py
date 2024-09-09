"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
"""

import logging

from swing.http_generator.httpgenerator.utils.utils import Utils


def get_logger():
    logger = logging.getLogger('swingLogger')
    # 每次被调用后，清空已经存在handler
    logger.handlers.clear()

    logger.setLevel(logger.level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logger.level)

    format_str = "%(asctime)-15s %(levelname)s"
    date_format_str = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format_str)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def log_print(func):
    def log(*args, **kwargs):
        result = func(*args, **kwargs)
        logger = get_logger()
        if result.status_code != 200:
            logger.warning("请求失败! 失败的resp为: {0}".format(result.text))
        logid = result.headers.get("Trace-Id", None)
        logger.info("请求的接口地址为: {0}, logid为: {1}, 执行环境为: {2}".format(kwargs.get("url", None), logid, Utils.get_env_label()))
        return result

    return log