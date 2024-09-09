"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/18 下午7:39
@Author: xingyun
"""
import json
import requests

from rpc_generator.utils.utils import Utils
from rpc_generator.plugins.log.logger import logger


class FeiShu(object):
    def __init__(self):
        utils = Utils()
        self.app_id = utils.get_git_conf('feishu', 'app_id')
        self.token_url = utils.get_git_conf('feishu', 'token_url')
        self.app_secret = utils.get_git_conf('feishu', 'app_secret')
        if 'feishu' in utils.get_section_key():
            self.spreadsheetToken = utils.get_conf('feishu', 'spreadsheetToken')
        else:
            # 走兜底
            self.spreadsheetToken = utils.get_git_conf('feishu', 'spreadsheetToken')

    def get_token(self) -> str:
        token_url = self.token_url
        header_params = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        # 请求体
        body_params = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            logger.info(f'========= start get token ==========')
            # 发送 POST 请求
            response = requests.post(token_url, headers=header_params, data=json.dumps(body_params))
            # 检查请求是否成功
            response.raise_for_status()
            if json.loads(response.text)['code'] == 0:
                logger.info(response.text)
                return json.loads(response.text)['tenant_access_token']
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return ''

    def get_sheet_id(self, spread_sheet_token=None) -> list:
        sheet_list = []
        if spread_sheet_token is None:
            spread_sheet_token = self.spreadsheetToken
        sheet_url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spread_sheet_token}/metainfo'
        header_params = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self.get_token()}'
        }
        try:
            logger.info(f'========= start get sheet id ==========')
            # 发送 POST 请求
            response = requests.get(sheet_url, headers=header_params)
            # 检查请求是否成功
            response.raise_for_status()
            if json.loads(response.text)['code'] == 0:
                logger.info('========= get sheet id response ==========')
                logger.info(response.text)
                for sheet in json.loads(response.text)['data']['sheets']:
                    sheet_dict = {sheet['title']: sheet['sheetId']}
                    sheet_list.append(sheet_dict)
                return sheet_list
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return []

    def get_sheet_info(self, spread_sheet_token=None, sheet_id=None) -> dict:
        """
        :param sheet_id: 要获取某一sheet的内容
        :return dict = [
            {
                'path': 'test',
                'env': 'test',
                'query_params': 'test',
                'body_params': 'test',
                'assert': 'test',
                'mark': 'test'
            }, {}, {}, {}
        ]
        """
        sheet_info_list = []
        if spread_sheet_token is None:
            spread_sheet_token = self.spreadsheetToken
        sheet_info_url = (f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/'
                          f'{spread_sheet_token}/values/{sheet_id}?valueRenderOption=ToString')
        header_params = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': f'Bearer {self.get_token()}'
        }
        # todo
        if sheet_id is None:
            # sheet_id未传，获取所有的表格信息
            return self.get_sheet_id()
        # 正常处理
        try:
            logger.info(f'========= start get sheet info ==========')
            # 发送 POST 请求
            response = requests.get(sheet_info_url, headers=header_params)
            # 检查请求是否成功
            response.raise_for_status()
            if json.loads(response.text)['code'] == 0:
                logger.info('========= get sheet info response ==========')
                logger.info(response.text)
                values = json.loads(response.text)['data']['valueRange']['values']
                # 遍历values数组，跳过第一行（通常是列标题）
                for row in values[1:]:
                    # 创建一个字典，键为values数组第一行的值，值为当前行的值
                    row_dict = {values[0][i]: row[i] for i in range(len(row))}
                    # 将字典添加到结果列表中
                    sheet_info_list.append(row_dict)
                logger.info(f'========== sheet_info_list is =======\n{sheet_info_list}' )
                return sheet_info_list
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return []


if __name__ == '__main__':
    # sheet_inf = FeiShu().get_sheet_id()
    # logger.info(f'token: {sheet_inf}')
    voice_type = '系统音色'
    voice_id_list = []
    sheet_info_list = FeiShu().get_sheet_id('IPrTsmcK8hPquCtYaLJclyVQnFd')
    for sheet_info in sheet_info_list:
        for key, value in sheet_info.items():
            if key == voice_type:
                voice_list = FeiShu().get_sheet_info('IPrTsmcK8hPquCtYaLJclyVQnFd', value)
                logger.info(voice_list)
                for voice in voice_list:
                    voice_id_list.append(voice['voice_id'])
    logger.info(voice_id_list)




