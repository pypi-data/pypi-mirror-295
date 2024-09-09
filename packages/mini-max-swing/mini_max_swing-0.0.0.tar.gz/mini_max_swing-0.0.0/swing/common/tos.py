"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/4 下午3:14
@Author: xingyun
"""
import requests
import sys
import logging

from allure_report_common.util import Util

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError


# 官方API文档：https://cloud.tencent.com/document/product/436/65824
class Tos(object):
    def __init__(self):
        self.cos_secret_id = 'AKIDYDpHYeaKtIYjniQIGKQbq4W1NZcpWDyS'
        self.cos_secret_key = 'sfKtjgbYI9vWdQAx6UwSwKbojqBZ2eDs'
        self.cos_region = 'ap-shanghai'
        self.cos_bucket = 'qa-tool-1315599187'
        self.app_id = '1315599187'
        self.client = self.tos_init_client()

    def tos_init_client(self):
        # 正常情况日志级别使用 INFO，需要定位时可以修改为 DEBUG，此时 SDK 会打印和服务端的通信信息
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        secret_id = self.cos_secret_id
        secret_key = self.cos_secret_key
        region = 'ap-shanghai'
        token = None
        scheme = 'https'
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        client = CosS3Client(config)
        return client

    def get_tos_list(self) -> list:
        client = self.client
        bucket_lists = client.list_buckets()
        logging.info('=====bucket_lists======')
        logging.info(bucket_lists)
        return bucket_lists

    # 获取bucket 指定目录下面的的对象
    def get_info_from_dir(self, bucket_name: str, dir_name: str):
        client = self.client
        if dir_name.startswith('/'):
            dir_name = dir_name[1:]
        if not dir_name.endswith('/'):
            dir_name += '/'
        # 列举 dir_name 目录下的文件和子目录
        response = client.list_objects(
            Bucket=bucket_name, Prefix=dir_name, Delimiter='/')
        # 打印文件列表
        if 'Contents' in response:
            for content in response['Contents']:
                logging.info(content['Key'])
        # 打印子目录
        if 'CommonPrefixes' in response:
            for folder in response['CommonPrefixes']:
                logging.info(folder['Prefix'])

    def get_info_from_bucket(self, bucket_name: str) -> list:
        client = self.client
        response = client.list_objects(Bucket=bucket_name)
        logging.info('=====bucket_lists======')
        logging.info(response)
        if 'Contents' in response:
            for content in response['Contents']:
                logging.info(content['Key'])
        return response['Contents']

    def put_object_to_bucket_with_easy(self, file_path: str, bucket_name: str, file_name: str) -> None:
        client = self.client
        # 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
        with open('picture.jpg', 'rb') as fp:
            response = client.put_object(
                LocalFilePath=file_path,
                Bucket=bucket_name,
                Body=fp,
                Key=file_name,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        logging.info(response['ETag'])

    def put_object_to_bucket_with_bytes(self, file_path: str, bucket_name: str, file_name: str) -> None:
        client = self.client
        # 字节流简单上传
        response = client.put_object(
            LocalFilePath=file_path,
            Bucket=bucket_name,
            Body=b'bytes',
            Key=file_name,
            EnableMD5=False
        )
        logging.info(response['ETag'])

    def put_object_to_bucket_with_chunk(self, file_path: str, bucket_name: str, file_name: str) -> None:
        client = self.client
        # chunk 简单上传
        stream = requests.get('https://cloud.tencent.com/document/product/436/7778')

        # 网络流将以 Transfer-Encoding:chunked 的方式传输到 COS
        response = client.put_object(
            LocalFilePath=file_path,
            Bucket=bucket_name,
            Body=stream,
            Key=file_name
        )
        logging.info(response['ETag'])

    def put_object_to_bucket(self, bucket_name: str, local_path: str, file_name: str) -> None:
        # 高级上传接口（推荐）
        client = self.client
        # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
        response = client.upload_file(
            Bucket=bucket_name,
            LocalFilePath=local_path,
            Key=file_name,
            PartSize=1,
            MAXThread=10,
            EnableMD5=False
        )
        logging.info(response['ETag'])

    def dir_to_create(self,  bucket_name: str, dir_name: str) -> None:
        client = self.client
        # 创建目录
        if not dir_name.endswith('/'):
            dir_name = dir_name + '/'
        logging.info('=====dir_to_create=====')
        logging.info(dir_name)
        response = client.put_object(
            Bucket='qa-tool-1315599187',
            Key=dir_name,
            Body=b''
        )
        logging.info(response)

    def dir_to_delete(self, bucket_name: str, to_delete_dir: str) -> None:
        client = self.client
        if to_delete_dir.startswith('/'):
            to_delete_dir = to_delete_dir[1:]
        if not to_delete_dir.endswith('/'):
            to_delete_dir += '/'
        # 删除指定前缀 (prefix)的文件
        while True:
            response = client.list_objects(Bucket=bucket_name, Prefix=to_delete_dir, Marker="")
            if 'Contents' in response:
                for content in response['Contents']:
                    print("delete object: ", content['Key'])
                    client.delete_object(Bucket=bucket_name, Key=content['Key'])

            if response['IsTruncated'] == 'false':
                break

            marker = response['NextMarker']

        logging.info('===================')
        logging.info(response)

    def exists_object(self, bucket_name: str, file_name: str) -> bool:
        client = self.client
        response = client.object_exists(
            Bucket=bucket_name,
            Key=file_name)
        logging.info('====exists object response is ====== :')
        logging.info(response)
        return response

    def download_file(self, bucket_name: str, file_path: str, dest_file_path: str) -> None:
        client = self.client
        # 使用高级接口断点续传，失败重试时不会下载已成功的分块(这里重试10次)
        for i in range(0, 10):
            try:
                response = client.download_file(
                    Bucket=bucket_name,
                    Key=file_path,
                    DestFilePath=dest_file_path)
                break
            except CosClientError or CosServiceError as e:
                logging.info(e)


if __name__ == '__main__':
    tos = Tos()
    data_time = Util.time_formatted()
    bucket_ = "qa-tool-1315599187"
    # delete_dir = '/swingReport/20240614/'
    # tos.get_info_from_dir(bucket_name=bucket_, dir_name=delete_dir)
    # tos.dir_to_delete(bucket_name=bucket_, to_delete_dir=delete_dir)
    tos.get_info_from_bucket(bucket_)

    # tos.get_info_from_bucket(bucket_)
    # logging.info('=====bucket_lists======')
    # tos.get_info_from_dir(bucket_, 'swingReport')
    # tos.exists_object(bucket_, 'swingReport/20240604/swing_report_20240604_123456.zip')

