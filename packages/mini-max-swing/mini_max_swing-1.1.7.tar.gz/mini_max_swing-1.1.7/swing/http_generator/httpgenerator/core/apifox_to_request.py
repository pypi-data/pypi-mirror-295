"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 15:31
@Author: xingyun
"""
import json


class ApiToRequest:
    def __init__(self):
        pass

    def parse_api_spec_from_file(self, file_path):
        # 打开文件并读取内容
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                api_spec = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []

        # 初始化结果列表
        result = []

        # 遍历 paths 中的每个路径
        for path, methods in api_spec['paths'].items():
            for method, details in methods.items():
                # 获取当前路径和方法的信息
                path_info = {
                    'method': method.upper(),
                    'path': path,
                    'header': {},
                    'req_schema': {
                        "body_param": {},
                        "query_param": {},
                        "files": {},
                        "form_data": {}
                    },
                    'resp_schema': {}
                }

                # 检查请求体内容类型
                request_body = details.get('requestBody', {})
                if request_body:
                    content_types = request_body.get('content', {})
                    for content_type, content_details in content_types.items():
                        if content_type == 'application/json':
                            path_info['req_schema']['body_param'] = self.get_properties_from_schema(
                                content_details.get('schema', {}))
                        elif content_type == 'multipart/form-data':
                            path_info['req_schema']['form_data'] = self.get_properties_from_schema(
                                content_details.get('schema', {}))

                # 遍历 parameters 列表
                for param in details.get('parameters', []):
                    # 根据参数类型分类参数
                    if param.get('in') == 'query':
                        path_info['req_schema']['query_param'][param['name']] = ApiToRequest.get_param_info(param)
                    elif param.get('in') == 'header':
                        path_info['header'][param['name']] = ApiToRequest.get_param_info(param)

                # 将路径信息添加到结果列表中
                result.append(path_info)
        return result

    @staticmethod
    def get_param_info(param):
        param_info = {
            'type': 'unknown',  # 默认类型为未知
            'optional': False,  # 默认为必填
            'children': {}
        }
        try:
            if 'example' in param:
                param_info['example'] = param['example']
            if 'schema' in param:
                schema = param['schema']
                param_info['type'] = schema.get('type', 'unknown')  # 使用schema中的type字段
                param_info['optional'] = True if param.get('required',
                                                           False) else False  # 根据required字段确定是否必填
                # 如果有子参数，可以在这里添加
                # param_info['children'] = self.get_properties_from_schema(schema.get('properties', {}))
        except KeyError as e:
            print(f"Missing key in parameter: {e}")
        return param_info

    @staticmethod
    def get_default_value(schema):
        try:
            if 'type' in schema:
                if schema['type'] == 'string':
                    return ''
                elif schema['type'] == 'integer':
                    return 0
                elif schema['type'] == 'boolean':
                    return False
                elif schema['type'] == 'array':
                    return []
                elif schema['type'] == 'object':
                    return {}
        except KeyError as e:
            print(f"Missing key in schema: {e}")
        return None

    def get_properties_from_schema(self, schema):
        try:
            properties = {}
            if 'properties' in schema:
                # 如果schema是一个对象，提取其属性
                for prop_name, prop_schema in schema['properties'].items():
                    prop_info = {
                        'type': prop_schema.get('type', 'unknown'),
                        'optional': True,
                        'children': {}
                    }
                    # 如果属性有子属性，递归处理
                    if 'properties' in prop_schema:
                        prop_info['children'] = self.get_properties_from_schema(prop_schema)
                    properties[prop_name] = prop_info
            return properties
        except KeyError as e:
            print(f"Missing key in schema: {e}")
        return {}


if __name__ == '__main__':
    data = ApiToRequest().parse_api_spec_from_file("/Users/minimax/Desktop/新产品平台Chat-User.openapi.json")
    print(data)
