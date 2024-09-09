#!/usr/bin/python
"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/27 14:25
@Author: xingyun
"""
import argparse
import logging
import os.path
from http_generator.httpgenerator.core.case_template import CaseTemplate
from http_generator.httpgenerator.core.data_template import DataTemplate
from http_generator.httpgenerator.core.code_template import CodeTemplate
from http_generator.httpgenerator.core.conf_template import ConfTemplate
from http_generator.httpgenerator.core.lib_template import LibTemplate
from http_generator.httpgenerator.core.apifox_to_request import ApiToRequest
from http_generator.httpgenerator.core.curl_to_request import CurlToRequest
from frametools.core.generate_file import GenerateFile
from rpc_generator.rpc_gen.rpcgenerator import RpcGenerator


parser = argparse.ArgumentParser(description="Case Generator.")
parser.add_argument('-operate', nargs='?', type=str, help='Please input operate，such as http、demo or rpc')
parser.add_argument('-psm', nargs='?', type=str, help='Please input psm, such as em.qa.venus.')
parser.add_argument('-version', nargs='?', type=str, help='Please input version, such as 1.0.0')
parser.add_argument('-branch', nargs='?', type=str, help='Please input branch, such as master')
parser.add_argument('-path', nargs='?', type=str,
                    help='Please input codepath、datapath、casepath、confpath, such as ys-chat')
parser.add_argument('-curl', nargs='?', type=str, help='Please input curl, such as curl --location '
                                                       '"https://gitlab.xaminim.com/api/v4/projects?private_token=E4czXB_ogWT9zkSSszEh"')
parser.add_argument('-apifox', nargs='?', type=str,
                    help='Please input apifox local_file_path, must xxx.json such as "/Users/minimax/Desktop/新产品平台Chat-User.apifox.json"')
parser.add_argument('-xray', nargs='?', type=str, help='Enable xray to report testcase deps')

args = parser.parse_args()


def generate_request_with_apifox():
    """
    :通过apifox请求来生成case
    """
    print('=====start generate_request_with_apifox =====')
    if not args.apifox:
        raise ValueError("-psm is required! please check")
    logging.info("======== start get api_list from apifox local_file_path =========")
    api_info = ApiToRequest().parse_api_spec_from_file(file_path=args.apifox)
    print("The api info is:\n", api_info)
    return api_info


def generate_request_with_curl():
    """
    :通过curl请求来生成case
    """
    logging.info('======== start generate_request_with_curl ========')
    if not args.curl:
        raise ValueError("-psm is required! please check")
    logging.info("======== start get api_list from csv local_file_path =========")
    api_info = CurlToRequest.parse_curls_from_csv(csv_path=args.curl)
    return api_info


def generate_template_http(api_info):
    if api_info:
        CodeTemplate().generate_template(psm=args.psm, api_info=api_info,
                                         code_dest_directory=args.path,
                                         version=args.version, xray=args.xray)
        DataTemplate().generate_template(psm=args.psm, api_info=api_info,
                                         data_dest_directory=args.path,
                                         version=args.version)
        CaseTemplate().generate_template(psm=args.psm, case_dest_directory=args.path, api_info=api_info)
        ConfTemplate().generate_template(conf_dest_directory=args.path)
        LibTemplate().generate_template(lib_dest_directory=args.path)
    else:
        logging.error("place check api_info first!")


def generator_demo_():
    logging.info("======== start generate_demo_file =========")
    GenerateFile.generate_demo()
    logging.info("======== generate_demo_file success ========")


if __name__ == '__main__':
    # 初始化框架，生成http对应的目录 并拉取对应的psm
    args.operate = "rpc"
    # args.apifox = "/Users/minimax/Desktop/QATOOLS.openapi.json"
    args.curl = "/Users/minimax/Desktop/curl_democsv.csv"
    # args.path = "ys"
    args.psm = "conversation_chat"
    if args.operate == "demo":
        generator_demo_()

    if args.operate == "http":
        generator_demo_()
        if args.curl:
            generate_template_http(api_info=generate_request_with_curl())
        if args.apifox:
            generate_template_http(api_info=generate_request_with_apifox())

    if args.operate == "rpc":
        generator_demo_()
        RpcGenerator().generate_rpc(args.psm)


def swing():
    # 初始化框架，生成http对应的目录 并拉取对应的psm
    # args.operate = "rpc"
    # args.curl = "/Users/minimax/Desktop/curl_democsv.csv"
    # args.path = "ys"
    # args.psm = "conversation_chat"
    if args.operate == "demo":
        generator_demo_()

    if args.operate == "http":
        generator_demo_()
        if args.psm:
            if args.curl:
                generate_template_http(api_info=generate_request_with_curl())
            if args.apifox:
                generate_template_http(api_info=generate_request_with_apifox())
        else:
            raise ValueError("-psm is required! please check")

    if args.operate == "rpc":
        generator_demo_()
        logging.info("======== start generate rpc  =========")
        RpcGenerator().generate_rpc(args.psm)



