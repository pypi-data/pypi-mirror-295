"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/25 15:31
@Author: xingyun
"""

import configparser as configparser


class ConfigParse(configparser.RawConfigParser):
    """
    框架中底层所使用的方法，业务一般不建议使用，解析器，用于解析config文件
    """
    def __init__(self, defaults=None):
        configparser.RawConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr
