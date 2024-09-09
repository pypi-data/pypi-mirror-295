"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:41
@Author: xingyun
"""
import logging
import os
import pathlib
import shutil
import base64
import re
import requests
from swing.rpc_generator.plugins.git.git import Git
from swing.rpc_generator.plugins.ptsd.parser import Parser
from swing.rpc_generator.utils.utils import Utils


class IdlDep:
    """
    用于处理thrift include的依赖文件
    """

    def __init__(self):
        self.git = Git()
        # 用于存储重名的include，防止无限递归
        self.rename_list = []

    def thrift_rewrite(self, dir):
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.thrift'):
                    logging.info(f"begin to rewrite file {file}")
                    content = ''
                    with open(os.path.join(root, file), 'r') as f:
                        for line in f:
                            if ('include "base.thrift"' in line) or ("/base.thrift" in line):
                                line = 'include "../../base.thrift"\n'
                            elif "include \"" in line:
                                for rename_thrift in self.rename_list:
                                    if rename_thrift["file"] == os.path.join(root, file) and rename_thrift["include_old"] in line:
                                        line = line.replace(rename_thrift["include_old"], rename_thrift["include_new"])
                                        break
                                line = line.replace("../", "")
                                if "/" in line and ("child_idls" not in line):
                                    valid_line = re.findall(r'\"(.*)\"', line)
                                    file_name = valid_line[0].split("/")[-1]
                                    if file_name != "base.thrift":
                                        line = f'include "{file_name}"\n'
                                if 'child_idls' in root:
                                    line = line.replace(" \"", " \"../")

                            content += line
                    with open(os.path.join(root, file), 'w') as wf:
                        wf.write(content)

    @staticmethod
    def get_include(thrift_file):
        includes = []
        with open(thrift_file, 'r') as fp:
            tree = Parser().parse(fp.read())
        # 初始化基本的树结构
        for include in tree.includes:
            include_value = os.path.split(include.path.value)
            if include_value[-1] != "base.thrift":
                includes.append(include_value)
        return includes

    def down_thrift_file(self, psm_service, git_path, biz, ref, data_path):
        """
        从git上下载thrift文件
        :param psm_service:
        :param git_path:
        :param biz:
        :return:
        """
        psm = psm_service.split('@')[0]
        dir_name = "_".join(psm_service.split(".")).replace('@', '_')
        file_name = f"{'_'.join(psm.split('.'))}.thrift"
        dir_path = os.path.join(os.getcwd(), data_path, "idls", biz, dir_name)
        file_path = os.path.join(dir_path, file_name)
        # 如果thrift文件已经存在，说明之前初始化过，非强制刷新的情况直接跳过不重复下载
        if os.path.isfile(os.path.join(dir_path, file_name)):
            print(f"psm:{psm} thrift file already exist!")
        else:
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
                pathlib.Path(os.path.join(dir_path, "__init__.py")).touch()
            file_name = f"{'_'.join(psm.split('.'))}.thrift"
            logging.info(f"begin to download {file_name}")
            # 如果文件不存在或者强制刷新，开始下载thrift文件
            self.git.gen_thrift_file(git_path, file_path, ref)
            logging.info(f"download {file_name} successful!")
        return file_path

    def download_dependence(self, thrift_file, git_root, branch="main"):
        includes = self.get_include(thrift_file)
        logging.info(f"begin to download {thrift_file}`s dependence")
        logging.info(f'includes is =============: {includes}')
        for include in includes:
            if include[0]:
                if ".." in include[0]:
                    level = include[0].count("..")
                    if len(include[0].split("..")[-1]) > 1:
                        name = f"{include[0].split('..')[-1]}/{include[-1]}"
                    else:
                        name = include[-1]
                    git_path = self.get_thrift_path(git_root, name, level)
                elif "." in include[0]:
                    name = include[-1]
                    git_path = self.get_thrift_path(git_root, name, 0)
            else:
                git_path = self.get_thrift_path(git_root, include[-1], 0)
            logging.info(f'== include is {include}, git_path is ==========:{git_path}')
            file_dir = os.path.dirname(thrift_file).replace('/child_idls', '')
            save_path = os.path.join(file_dir, include[-1])
            content = self.git.get_git_content(git_path, branch)
            if os.path.isfile(os.path.join(save_path)):
                with open(save_path, 'r') as old_file:
                    old_content = old_file.read()
                if old_content != content:
                    try:
                        os.mkdir(os.path.join(file_dir, "child_idls"))
                    except:
                        pass
                    rename_thrift = {"file": thrift_file,
                                     "include_old": include[-1] if include[0] == '' else f"{include[0]}/{include[-1]}",
                                     "include_new": f"child_idls/{include[-1]}"}
                    if not rename_thrift in self.rename_list:
                        self.rename_list.append(rename_thrift)
                    save_path = os.path.join(file_dir, "child_idls", include[-1])
            thrift_file = self.git.gen_thrift_file(git_path, save_path, branch)
            self.download_dependence(thrift_file, git_path, branch)

    def get_thrift_path(self, path, name, level=0):
        if level == 0:
            return os.path.join(os.path.dirname(path), name)
        for i in range(level + 1):
            path = os.path.dirname(path)
        name = name.replace('/', '', 1) if name.startswith('/') else name
        return os.path.join(path, name)

    def check_data_exist(self, data_dir):
        """
        判断项目根目录下是否存在data包
        """
        data_path = os.path.join(os.getcwd(), data_dir)
        file_path = os.path.join(data_path, '__init__.py')
        idls_path = os.path.join(data_path, 'idls')
        json_path = os.path.join(data_path, 'json')

        if not os.path.isdir(idls_path):
            os.makedirs(idls_path)
            with open(os.path.join(idls_path, '__init__.py'), 'w') as f:
                f.close()

        if not os.path.isdir(json_path):
            os.makedirs(json_path)
            with open(os.path.join(json_path, '__init__.py'), 'w') as f:
                f.close()

        if not os.path.exists(file_path):
            with open(os.path.join(file_path), 'w') as f:
                f.close()

        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        thrifts_path = os.path.join(root, 'thrifts')
        for file in os.listdir(thrifts_path):
            file_path = os.path.join(thrifts_path, file)
            if file.endswith('thrift') or file.endswith('pyi'):
                shutil.copy(file_path, idls_path)

    def down_thrift_by_api(self, psm_service, path, biz, branch, data_path, formation='json'):

        psm = psm_service.split('@')[0]

        dir_name = "_".join(psm_service.split(".")).replace('@', '_')
        root_file = "_".join(psm.split("."))
        [repo_name, f_path] = path.split('@')
        dir_path = os.path.join(os.getcwd(), data_path, "idls", biz, dir_name)

        params = {
            "repo_name": repo_name,
            "revision": branch,
            "file_path": f_path,
            "format": formation
        }

        root_name = f_path
        try:
            url = Utils.get_conf('ee_idl', 'url')
            resp = requests.get(url, params=params)
            resp_dict = resp.json()
            files = resp_dict.get('files', {})
            if resp.status_code != 200:
                # 尝试使用跨库方案请求
                resp = requests.get("https://codebase.byted.org/v2/idl/across/archive", params=params)
                resp_dict = resp.json()
                if resp.status_code != 200:
                    raise Exception(resp_dict)
                for _, codebase in resp_dict.items():
                    for _, repo in codebase.items():
                        files.update(repo['files'])
            for file, value in files.items():
                if '/base.thrift' in file or 'base.thrift' == file:
                    continue

                file_name = file.split('/')[-1]
                # 把根thrift文件名始终保持为p_s_m形式
                if file == root_name:
                    file_path = os.path.join(dir_path, '.'.join([root_file, 'thrift']))
                else:
                    file_path = os.path.join(dir_path, file_name)
                # 如果thrift文件已经存在，说明之前初始化过，非强制刷新的情况直接跳过不重复下载
                if os.path.isfile(file_path):
                    print(f"psm:{psm} thrift file already exist!")
                else:
                    if not os.path.isdir(dir_path):
                        os.makedirs(dir_path)
                        pathlib.Path(os.path.join(dir_path, "__init__.py")).touch()
                    logging.info(f"begin to download {file_name}")

                    content = base64.b64decode(value.get('content', '')).decode()
                    with open(file_path, 'w') as f:
                        f.write(content)

        except Exception as e:
            print(f"download thrift files failed for: {e}")
            raise e

        return os.path.join(dir_path, '.'.join([root_file, 'thrift']))


if __name__ == "__main__":
    idl_dep = IdlDep()
    # idl_dep.check_data_exist()
    # psm = 'ys-chat'
    # git_path1 = 'data/chat/chat_service.thrift'
    # idl_dep.down_thrift_file(psm, git_path, 'demand', 'master')
    # idl_dep.download_dependence(thrift_file, git_path1)
    idl_dep.thrift_rewrite(
        '/Users/xingyun/.pyenv/versions/3.7.2/lib/python3.7/site-packages/rpcgenerator/core/data/idls/ys-chat')
