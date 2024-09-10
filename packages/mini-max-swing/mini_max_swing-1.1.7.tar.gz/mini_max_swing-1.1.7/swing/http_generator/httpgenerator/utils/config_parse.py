"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
"""

import configparser as configparser


class ConfigParse(configparser.RawConfigParser):
    def __init__(self, defaults=None):
        configparser.RawConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr
