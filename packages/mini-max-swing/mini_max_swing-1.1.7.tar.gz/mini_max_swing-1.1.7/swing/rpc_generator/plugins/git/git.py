"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/26 14:24
@Author: xingyun
"""

import os
import re

import gitlab
from swing.rpc_generator.utils.utils import Utils


class Git:

    def __init__(self):
        project_id = Utils.get_git_conf("gitlab", "project_id")
        private_token = Utils.get_git_conf("gitlab", "private_token")
        url = Utils.get_git_conf("gitlab", "git_host")
        git = gitlab.Gitlab(url=url, private_token=private_token)
        self.project = git.projects.get(project_id)

    def gen_thrift_file(self, git_path, save_path, ref="main"):
        if os.path.isfile(save_path):
            print(f"{save_path} already exist!")
            return save_path
        content = self.project.files.get(file_path=git_path, ref=ref)
        content_str = content.decode().decode()
        with open(save_path, 'w') as f:
            content_str = Git.add_field_numbering(content_str)
            f.write(content_str)
        return save_path

    def get_git_content(self, git_path, ref="main"):
        content = self.project.files.get(file_path=git_path, ref=ref)
        return content.decode().decode()

    @staticmethod
    def add_field_numbering(idl_str):
        # 正则表达式匹配 struct 的模式
        struct_pattern = re.compile(r'struct\s+(\w+)\s*{([^}]*)}', re.DOTALL)

        # 正则表达式匹配已经有编号的字段
        numbered_field_pattern = re.compile(r'^\d+:', re.MULTILINE)

        def replace_struct(match):
            struct_name = match.group(1)
            fields = match.group(2).strip().split('\n')

            # 如果 struct 中只有一个字段，则检查是否缺少编号
            if len(fields) == 1:
                field = fields[0].strip()
                if not numbered_field_pattern.match(field):
                    # 如果字段没有编号，则添加编号
                    field = f'1: {field}'
                return f'struct {struct_name} {{\n    {field}\n}}'

            # 如果 struct 中有多个字段，则保持不变
            return match.group(0)

        # 替换 IDL 字符串中的 struct
        updated_idl_str = struct_pattern.sub(replace_struct, idl_str)
        return updated_idl_str


if __name__ == "__main__":
    git = Git()
