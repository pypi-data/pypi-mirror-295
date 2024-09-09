"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/25 15:31
@Author: xingyun
"""

import os
import re
import requests
from urllib import request


class FormDataUtils(object):
    @staticmethod
    def read_network_file(file_path):
        """
        使用场景：读取远端文件
        :param file_path: 文件地址
        :return: tuple格式数据:([文件名]， [文件])
        """
        if re.match(r'^https?:/{2}\w.+$', file_path):
            try:
                request.urlopen(file_path)
            except Exception as e:
                print(e)
                print(file_path + "无效")
                raise
            else:
                file_name = file_path.split('/')[-1]
                res = requests.get(file_path)
                fields = (file_name, res.content)
        else:
            raise FileExistsError(f'文件存储的链接有误')

        return fields

    @staticmethod
    def download_network_file(file_path):
        """
        使用场景：将远端文件下载到本地
        :param file_path: 文件下载地址
        :return:无
        """
        if re.match(r'^https?:/{2}\w.+$', file_path):
            try:
                request.urlopen(file_path)
            except Exception as e:
                print(e)
                print(file_path + "无效")
                raise
            else:
                file_name = file_path.split('/')[-1]
                path = "./file/"
                if not (os.path.exists(path)):
                    os.makedirs(path)
                download_path = path + file_name
                if not os.path.exists(download_path):
                    res = requests.get(file_path)
                    with open(download_path, 'wb') as f:
                        f.write(res.content)
        else:
            raise FileExistsError(f'文件存储的链接有误')

    @staticmethod
    def read_file(file_path):
        """
        使用场景：读取本地文件
        :param file_path: 文件地址
        :return: tuple格式数据:([文件名]， [文件])
        """
        if os.path.isfile(file_path):
            head, tail = os.path.split(file_path)
            fields = (tail, open(file_path, "rb"))
        else:
            raise FileExistsError(f'文件不存在，请检查文件路径是否有误')
        return fields
