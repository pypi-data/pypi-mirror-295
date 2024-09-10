"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:47
@Author: xingyun
"""
import logging
import os
import sys
from enum import Enum
from swing.rpc_generator.plugins.ptsd.parser import Parser
from swing.rpc_generator.plugins.ptsd.ast import Struct, Service, Enum

sys.setrecursionlimit(100)


class ThriftParser:
    COMMONTYPE = ["i16", "i32", "i64", "bool", "byte", "double", "string"]
    COMMON_MAPPING = {"i16": 0, "i32": 0, "i64": 0, "bool": False, "byte": "", "double": 0.0, "string": ""}

    def __init__(self, psm):
        self.psm = psm

    def traverse_tree(self, dir, file):
        with open(os.path.join(dir, file), 'r') as fp:
            tree = Parser().parse(fp.read())
        # 初始化基本的树结构
        # print("os.path.join(dir, file)", os.path.join(dir, file))
        nodes = {"service": {}, "structs": [], "enums": [], "includes": [], "namespaces": []}
        for include in tree.includes:
            # 如果该thrift文件中有include引用，递归添加所有的引用数据，统一放在includes节点
            include_name = os.path.split(include.path.value)[-1]
            if os.path.split(include.path.value)[-1] == "base.thrift":
                ret = self.traverse_tree(os.path.join(dir, "../../.."), include_name)
            elif "child_idls" in include.path.value:
                ret = self.traverse_tree(dir, include_name)
            else:
                ret = self.traverse_tree(dir, include_name)
            nodes["includes"].append(ret)
        # 定义namespace空间
        for namespace in tree.namespaces:
            nodes["namespaces"].append(namespace.name.value)
        # 开始遍历body
        for node in tree.body:
            # 处理struct结构
            if isinstance(node, Struct):
                # 处理struct
                struct = {"name": node.name.value, "type": '.'.join([file.split(".")[0], node.name.value]),
                          "fields": [{"name": field.name.value,
                                      "type": str(field.type)
                                      if '.' in str(field.type) or str(field.type) in self.COMMONTYPE
                                      else '.'.join([file.split(".")[0], str(field.type)]),
                                      "required": field.required
                                      } for field in node.fields]}

                nodes["structs"].append(struct)
            # 处理service结构
            elif isinstance(node, Service):
                # 处理service
                nodes["service"]["name"] = node.name.value
                nodes["service"]["functions"] = []
                for function in node.functions:
                    fun = {"name": function.name.value}

                    try:
                        fun["response"] = function.type.value
                    except AttributeError as e:
                        fun["response"] = function.type
                    except Exception as e:
                        raise e
                    # if isinstance(function.type, String) or isinstance(function.type, Bool) else function.type.value
                    fun["arguments"] = [{"name": arg.name.value, "type": str(arg.type)} for arg in function.arguments]
                    nodes["service"]["functions"].append(fun)
            elif isinstance(node, Enum):
                # 处理enum结构
                enum = {"name": '.'.join([file.split(".")[0], node.name.value]),
                        "values": [str(value.name) for value in node.values]}

                nodes["enums"].append(enum)

        return nodes

    def get_struct_json(self, node_json, psm, thrift_name=None):
        """
        :des 获取结构化的json数据
        :param psm
        :param thrift_name
        :param node_json:
        :return: struct_json
        """

        struct_json = {"psm": psm, "result": []}
        service = {"service_name": node_json["service"]["name"], "method": []}
        type_prefix = psm if thrift_name is None else thrift_name
        for function in node_json["service"]["functions"]:
            method = {"name": function["name"]}
            request_type = function["arguments"][0]["type"] if function["arguments"] else None
            method["request_name"] = request_type
            try:
                if not request_type:
                    method["request_json"] = {}
                else:
                    method["request_json"] = self.get_request_json(node_json,
                                                               '.'.join([type_prefix.replace('.', '_'), request_type]))
            except RecursionError as e:
                raise e
            except Exception as e:
                logging.info("get_struct_json error", e)
                continue

            service["method"].append(method)
        struct_json["result"].append(service)
        for method in struct_json["result"][0]["method"]:
            for key, value in method["request_json"].items():
                if value == [{}]:
                    method["request_json"][key] = []
        return struct_json

    def get_request_json(self, node_json, name, parent=None, level=0, recursive_path=[]):
        recursive_path.append(name)
        for recursive_item in recursive_path:
            if recursive_path.count(recursive_item) >= 3:
                recursive_path.pop(-1)
                return {}
        request_json = {}
        structs = node_json["structs"]

        if name.split('.')[-1] in self.COMMONTYPE:
            recursive_path.pop(-1)
            return ThriftParser.COMMON_MAPPING[name.split('.')[-1]]

        for struct in structs:
            if struct["type"] == name:
                # 开始遍历字段
                if self.psm.replace('.', '_') in struct["type"]:
                    request_json["__type"] = struct["type"].split('.')[-1]
                else:
                    request_json["__type"] = struct["type"]
                for field in struct["fields"]:
                    # 设置字段初始值
                    request_json[field['name']] = {}
                    # 如果是基础类型，给基础类型赋空值
                    if field["type"] in ThriftParser.COMMONTYPE:
                        if field["required"]:  # 如果该类型是必须 required
                            request_json[field['name']] = ThriftParser.COMMON_MAPPING[
                                field["type"]]
                        request_json[field['name']] = ThriftParser.COMMON_MAPPING[
                            field["type"]]
                    elif field['type'] in [_enum['name'] for _enum in node_json['enums']]:
                        if field["required"]:
                            request_json[field['name']] = ""
                        # 处理嵌套引用
                    elif ''.join(['<', struct['name'], '>']) in field['type'] or struct['name'] == field['type'] or \
                            struct['type'] == field['type']:
                        request_json[field['name']] = self.get_struct_para(struct, field, level=level)
                    elif parent and parent.split('.')[-1] in field["type"]:
                        if 'list<' in field["type"]:
                            request_json[field['name']] = []
                        else:
                            request_json[field['name']] = {}
                    else:
                        if "list<" in field["type"]:
                            if "list<list" in field["type"]:
                                ret = self.get_list_para(node_json, field)
                                request_json[field["name"]] = ret
                            else:
                                ret = self.get_list_para(node_json, field)
                                request_json[field["name"]] = ret
                        elif "map<" in field["type"]:
                            ret = self.get_map_para(node_json, field)
                            request_json[field["name"]] = ret
                        else:
                            # 如果是非基础类型，则递归调用
                            ret = self.get_request_json(node_json, field["type"], parent=name, level=level,
                                                        recursive_path=recursive_path)
                            if ret:
                                request_json[field["name"]] = ret
                            else:
                                # 如果在body体中没有找到strut，说明是include进来的数据，需要去include中查找
                                for include in node_json["includes"]:
                                    ret = self.get_request_json(include, field["type"], parent=name, level=level,
                                                                recursive_path=recursive_path)
                                    if ret or ret == '':
                                        request_json[field["name"]] = ret
                                        break

        # 处理枚举引入
        if name in [_enum['name'] for _enum in node_json['enums']]:
            recursive_path.pop(-1)
            return ""
        # 处理嵌套引用
        # 处理跨文件引用的struct
        if len(name.split('.')) > 1 and request_json == {}:
            for include in node_json['includes']:
                ret = self.get_request_json(include, '.'.join(name.split('.')[1:]), level=level,
                                            recursive_path=recursive_path)
                if ret != {}:
                    recursive_path.pop(-1)
                    return ret
        recursive_path.pop(-1)
        return request_json

    def get_list_para(self, node_json, field):
        """
        :desc:处理list类型的参数
        :param node_json:
        :param field:
        :return:
        """
        if "list<list<" in field["type"]:
            list_para = field["type"].split('.')[-1].replace("list<list<", "").replace(">>", "")
            if list_para in ThriftParser.COMMONTYPE:
                ret = [[]]
            else:
                ret = [[self.get_request_json(node_json, list_para)]]
                if not ret:
                    for include in node_json["includes"]:
                        ret = self.get_request_json(include, list_para)
                        if ret:
                            ret = [[ret]]
                            break
        elif "list<" in field["type"]:
            list_para = field["type"].replace("list<", "").replace(">", "").split('.')[-1]
            if list_para in ThriftParser.COMMONTYPE:
                ret = []
            else:
                ret = [self.get_request_json(node_json, list_para)]
                if not ret or ret == [{}]:
                    for include in node_json["includes"]:
                        ret = self.get_request_json(include, list_para)
                        if ret:
                            ret = [ret]
                            break

        return ret

    def get_map_para(self, node_json, field):
        """
        :desc：处理map类型的参数
        :param node_json:
        :param field:
        :return:
        """
        ret = {}
        if "map<" in field["type"]:
            key = field["type"][4:-1].split(",")[0].strip()
            value = field["type"][4:-1].split(",")[-1].strip()
            if value in ThriftParser.COMMONTYPE:
                ret[f"<{key}>"] = ""
                # ret[key] = ""
            else:
                # 如果是非基础类型，则递归调用
                # ret[key] =  self.get_request_json(node_json, value)
                ret[f"<{key}>"] = self.get_request_json(node_json, value)
                if not ret[f"<{key}>"]:
                    # 如果在body体中没有找到strut，说明是include进来的数据，需要去include中查找
                    for include in node_json["includes"]:
                        # ret[key] = self.get_request_json(include, field["type"].split(".")[-1])
                        map_val = self.get_request_json(include, value.split(".")[-1])
                        if map_val:
                            ret[f"<{key}>"] = map_val
                            # print(key, "value.split", value, ret[f"<{key}>"] )
        return ret

    def get_struct_para(self, struct, field, level):
        node_json = {
            "structs": [struct],
            "enums": [],
            "includes": [],
            "namespaces": []
        }
        if "list<" in field['type']:
            if level == 0:
                ret = [self.get_request_json(node_json, struct['type'], level=1)]
            else:
                ret = []
        elif "map<" in field['type']:
            ret = {}
        elif struct['name'] == field['type'] or struct['type'] == field['type']:
            if level == 0:
                ret = self.get_request_json(node_json, struct['type'], level=1)
            else:
                ret = {}
        else:
            ret = ""
        return ret


if __name__ == "__main__":
    thrift1 = ThriftParser('data.ys-chat')

    test = thrift1.traverse_tree(
        "/Users/minimax/PycharmProjects/generator_rpc/data/idls/ys/ys_chat/ys_chat.thrift")
    # test = thrift1.traverse_tree(os.path.join(os.getcwd(), "data", "idls", "search", "ea_cd_searchpage"),
    #                              "ea_cd_searchpage.thrift")
    print(test)
    # print(json.dumps(thrift1.get_struct_json(test)))

