"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
@description：模板创建 可以复制demo文件夹中的文件
"""

import os
import shutil


class GenerateFile(object):
    @staticmethod
    def generate_demo():
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_file_path = os.path.join(root_path, 'demo')
        files = os.listdir(parent_file_path)
        for file in files:
            src_file_path = os.path.join(root_path, 'demo', file)
            target_file_path = os.path.join(os.getcwd(), file)

            # 判断路径对应的文件是否是文件夹
            if os.path.isdir(src_file_path):
                # 判断目标路径下是否存在文件夹
                if os.path.exists(target_file_path):
                    shutil.rmtree(target_file_path)
                    shutil.copytree(src_file_path, target_file_path)
                else:
                    shutil.copytree(src_file_path, target_file_path)
