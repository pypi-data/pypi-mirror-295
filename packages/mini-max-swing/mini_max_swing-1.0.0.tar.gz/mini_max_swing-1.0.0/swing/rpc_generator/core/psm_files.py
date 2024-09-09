"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/23 15:41
@Author: xingyun
"""

import os
import shutil
from rpc_generator.utils.utils import Utils
from rpc_generator.core.idl_dep import IdlDep
from rpc_generator.core.gen_service import gen_service
from rpc_generator.core.gen_case import gen_case
from rpc_generator.plugins.log.logger import logger
from rpc_generator.core.gen_conf import ConfTemplate
from rpc_generator.core.thrift_parser import ThriftParser


class PsmFiles:
    @staticmethod
    def gen_json_file(file_path, psm_service, biz, data_path, path):
        """
        生成json文件
        :param file_path:
        :param psm_service:
        :param biz:
        :param data_path:
        :param path:
        :return:
        """
        psm = psm_service.split('@')[0]
        file_name = f"{'_'.join(psm_service.split('.')).replace('@', '_')}.json"
        biz_dir = os.path.join(os.getcwd(), data_path, "json", biz)

        json_path = os.path.join(biz_dir, file_name)
        init_path = os.path.join(biz_dir, "__init__.py")

        if not os.path.exists(biz_dir):
            os.makedirs(biz_dir)
            with open(init_path, 'w') as inf:
                inf.close()

        # thrift_tag = None if '_'.join(psm.split('.')) == thrift_file.split('.')[0] else thrift_file.split('.')[0]
        # 判断某一对象(需提供绝对路径)是否为文件
        if os.path.isfile(json_path):
            print(f"psm:{psm} json file already exist!")
        else:
            logger.info(f"begin to gen json file {file_name}")
            if not os.path.exists(os.path.join(os.getcwd(), data_path, "json", biz)):
                os.makedirs(os.path.join(os.getcwd(), data_path, "json", biz))
            thrift = ThriftParser(psm)
            struct = thrift.traverse_tree(os.path.split(file_path)[0], os.path.split(file_path)[-1])
            json_data = ""
            try:
                json_data = thrift.get_struct_json(struct, psm)
            except Exception as e:
                logger.error(f"generate json file failed for: {e}")

            Utils.write_json(json_data, json_path)
            logger.info(f"gen json file {file_name} successful")
        return json_path

    @staticmethod
    def generate(psm_service, path, biz, branch, data_dir, module_dir, case_dir, conf_path, force=True, xray=""):
        """
        生成psm所需要的所有文件
        :param psm_service
        :param path:
        :param biz:
        :param branch:
        :param data_dir:
        :param module_dir:
        :param case_dir:
        :param conf_path:
        :param force:
        :param xray:
        :return:
        """
        if '@' in psm_service:
            [psm, service] = psm_service.split('@')
        else:
            psm, service = psm_service, ''
        if force:
            try:
                # 删除thrift文件
                idl_dir_name = "_".join(psm_service.split("."))
                idl_dir_path = os.path.join(os.getcwd(), data_dir, "idls", biz, idl_dir_name)
                shutil.rmtree(idl_dir_path)
                # 删除json文件
                json_file_name = f"{'_'.join(psm_service.split('.'))}.json"
                json_path = os.path.join(os.getcwd(), data_dir, "json", biz, json_file_name)
                os.remove(json_path)
                # 删除module文件
                module_file_name = f"{'_'.join(psm_service.split('.'))}.py"
                module_path = os.path.join(os.getcwd(), module_dir, biz, module_file_name)
                os.remove(module_path)
                # 删除case文件
                case_file_name = f"{'_'.join(psm_service.split('.'))}.py"
                case_path = os.path.join(os.getcwd(), case_dir, biz, case_file_name)
                os.remove(case_path)
                logger.info(f"force refresh success")
            except Exception as e:
                logger.error(f"force refresh error, may the target file does`t exist! error  for: {e}")

            # 生成thrift文件
            idl_dep = IdlDep()
            idl_dep.check_data_exist(data_dir)
            if '@' in path:
                idl_file_path = idl_dep.down_thrift_by_api(psm_service, path, biz, branch, data_dir)
            else:
                idl_file_path = idl_dep.down_thrift_file(psm_service, path, biz, branch, data_dir)
                idl_dep.download_dependence(idl_file_path, path, branch)
            idl_dep.thrift_rewrite(os.path.dirname(idl_file_path))
            # 生成json文件
            # namespace = os.path.split(idl_file_path)[-1].replace('.thrift', '')
            json_path = PsmFiles.gen_json_file(idl_file_path, psm_service, biz, data_dir, path)
            # 生成module文件
            gen_service(psm_service, branch, json_path, biz, data_dir, module_dir, xray)
            # 生成case文件
            gen_case(psm_service, json_path, biz, module_dir, case_dir)
            # 生成conf文件
            ConfTemplate.generate_template(conf_path)
        else:
            print("generator force refresh is off, exit...")
