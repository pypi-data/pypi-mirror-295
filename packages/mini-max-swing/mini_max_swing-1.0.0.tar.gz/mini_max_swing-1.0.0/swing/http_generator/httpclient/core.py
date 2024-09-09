"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/26 16:11
@Author: xingyun
"""
import requests
from requests.adapters import HTTPAdapter

from http_generator.httpgenerator.utils.logger import log_print
from http_generator.httpgenerator.utils.tlb import TLB


class HTTPClient:
    def __init__(self, timeout=8):
        """
        :param timeout: 每个请求的超时时间
        """
        s = requests.Session()
        #: 在session实例上挂载Adapter实例, 目的: 请求异常时,自动重试
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        #: 设置为False, 主要是HTTPS时会报错, 为了安全也可以设置为True
        s.verify = False
        #: 挂载到self上面
        self.s = s
        self.timeout = timeout

    @log_print
    def get(self, url=None, params=None, json_data=None, headers=None, files=None, cookies=None):
        """GET
        :param params
        :param json_data
        :param headers
        :param files
        :param cookies
        :param url:
        :return:
        """
        url, headers = TLB.adapt_tlb(url, headers)
        return self.s.get(url=url, params=params, json=json_data, headers=headers, files=files, cookies=cookies)

    @log_print
    def post(self, url=None, form_data=None, json_data=None, params=None, files=None, headers=None):
        """POST
        :param url:
        :param form_data: 有时候POST的参数是放在表单参数中
        :param json_data: 有时候POST的参数是放在请求体中(这时候 Content-Type: application/json )
        :param params: 有时候POST的参数是放在query参数中
        :param files: 有时候POST的参数是放在files参数中
        :param headers: 接口请求的headers
        :param stream: 是否使用流式请求
        :return:
        """
        url, headers = TLB.adapt_tlb(url, headers)
        return self.s.post(url=url, data=form_data, json=json_data, params=params, files=files, headers=headers)

    @log_print
    def put(self, url=None, form_data=None, json_data=None, params=None, headers=None, files=None):
        """PUT
        :param url:
        :param form_data: 有时候POST的参数是放在表单参数中
        :param json_data: 有时候POST的参数是放在请求体中(这时候 Content-Type: application/json )
        :param params: 有时候POST的参数是放在query参数中
        :param headers: 接口请求的headers
        :return:
        """
        url, headers = TLB.adapt_tlb(url, headers)
        if form_data:
            return self.s.put(url=url, data=form_data, params=params, headers=headers, files=files)
        if json_data:
            return self.s.put(url=url, json=json_data, params=params, headers=headers, files=files)
        return self.s.put(url=url, params=params, headers=headers, files=files)

    @log_print
    def delete(self, url=None, params=None, headers=None, files=None):
        """DELETE
        :param url:
        :param params: 一般GET的参数都是放在URL查询参数里面
        :return:
        """
        url, headers = TLB.adapt_tlb(url, headers)
        return self.s.delete(url=url, params=params, headers=headers, files=files)

    @log_print
    def patch(self, url=None, params=None, headers=None, files=None):
        """
        PATCH
        :param url:
        :param params:
        :param headers:
        :return:
        """
        url, headers = TLB.adapt_tlb(url, headers)
        return self.s.patch(url=url, params=params, headers=headers, files=files)

    def __del__(self):
        """当实例被销毁时,释放掉session所持有的连接
        :return:
        """
        if self.s:
            self.s.close()
