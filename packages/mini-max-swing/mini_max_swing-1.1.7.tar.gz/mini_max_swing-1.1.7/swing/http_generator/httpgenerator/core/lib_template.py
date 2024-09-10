"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 15:31
@Author: xingyun
"""
import logging
import os
from string import Template


class LibTemplate(object):
    _lib_string = '''# demo lib function
class Lib:
    @staticmethod
    def check_keyword(resp, keywords):
        """
        使用场景：校验返回值的关键字
        :param resp:需要校验关键字的返回值
        :param keywords:预期的关键字
        :return:无
        """
        assert len(resp) == len(keywords), f"校验返回值中的关键字长度失败，预期长度：{len(keywords)}，实际长度：{len(resp)}，全部的resp:{resp}"
        for key in keywords:
            if key not in resp:
                assert False, f"校验返回值中的关键字失败，未返回的关键字：{key}，全部的resp：{resp}"

    '''

    def __init__(self):
        pass

    def generate_template(self, lib_dest_directory=None):
        """
        生成模板方法
        :param lib_dest_directory: 生成数据模板的路径
        :return:
        """
        if not lib_dest_directory:
            lib_dest_directory = "lib"
        else:
            lib_dest_directory = f"lib/{lib_dest_directory}"
        abs_lib_path = os.path.join(os.getcwd(), lib_dest_directory)
        if not os.path.exists(abs_lib_path):
            lib_file_path = self.create_conf_file(lib_dest_directory)
            print("生成数据模板的路径为 :", lib_file_path)
            if lib_file_path:
                logging.info("创建数据文件成功!")
            else:
                logging.warning("创建数据文件失败!")
                return
            # 根据模版写入conf
            service_tmp_string = Template(LibTemplate._lib_string)
            content = service_tmp_string.substitute()
            with open(lib_file_path, 'a+') as f:
                f.write(content)
            logging.info(f"gen lib file {lib_dest_directory} successful")

    @staticmethod
    def create_conf_file(lib_dest_directory=None):
        """
        根据psm名称创建目录文件
        :param lib_dest_directory: 生成数据模板的目标绝对路径
        :return: 创建成功之后的*.py文件的绝对路径
        lib/ys/lib.py
        """
        lib_name = "lib.py"
        # 如果当前文件夹下对应path中提取的文件夹名称不存在，则创建该文件夹，并创建一个__init__.py文件
        if lib_dest_directory.startswith("/"):
            lib_dest_directory = lib_dest_directory[1:]
        if lib_dest_directory.endswith("/"):
            lib_dest_directory = lib_dest_directory[:-1]
        file_path = os.path.join(os.getcwd(), lib_dest_directory)  # conf/doukai

        if "/" in lib_dest_directory:
            dir_list = lib_dest_directory.split("/")
            path = os.getcwd()
            for dir_ in dir_list:
                path = os.path.join(path, dir_)
                if not os.path.exists(path):
                    os.makedirs(path)
                    open(path + "/__init__.py", "w")
                else:
                    if os.path.exists(path):
                        if not os.path.exists(path + "/__init__.py"):
                            open(path + "/__init__.py", "w")
        else:
            path = os.path.join(os.getcwd(), lib_dest_directory)
            if not os.path.exists(path):
                os.makedirs(path)
                open(path + "/__init__.py", "w")
            else:
                if not os.path.exists(path + "/__init__.py"):
                    open(path + "/__init__.py", "w")
        lib_file_path = os.path.join(file_path, lib_name)
        print(lib_file_path)
        if not os.path.isfile(lib_file_path):
            open(lib_file_path, "w", encoding='utf8')
        return lib_file_path


if __name__ == '__main__':
    conf_path = "conf/ys/"
    LibTemplate.create_conf_file()
