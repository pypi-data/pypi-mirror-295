"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
"""

import json
import os
import random
from urllib.parse import urlparse, urljoin

environ = os.environ
print("environ:" + str(environ))
gray = environ.get("gray")
domain = environ.get("domain")
channel = environ.get("channel")


class TLB(object):
    @staticmethod
    def is_tlb_task():
        if channel == 'TLB':
            return True
        return False

    @staticmethod
    def get_domain():
        if domain:
            return domain
        else:
            return ""

    @staticmethod
    def _get_a_ip_port(scheme="http"):
        try:
            ipList = json.loads(gray)
            item = ipList[0]["host_list"][0]
        except Exception as e:
            print(e.args)
            return TLB.get_domain()
        if scheme == "http":
            return "{}:{}".format(item["host"], item["port"])
        elif scheme == "https":
            return "{}:{}".format(item["host"], item["https_port"])
        else:
            return TLB.get_domain()

    @staticmethod
    def _get_a_random_ip_port(scheme="http"):
        try:
            ipList = json.loads(gray)
            item = random.choice(ipList[0]["host_list"])
        except Exception as e:
            print(e.args)
            return TLB.get_domain()
        if scheme == "http":
            return "{}:{}".format(item["host"], item["port"])
        elif scheme == "https":
            return "{}:{}".format(item["host"], item["https_port"])
        else:
            return TLB.get_domain()

    @staticmethod
    def get_new_url(url):
        url_parse = urlparse(url)
        new_netloc = TLB._get_a_ip_port(scheme=url_parse.scheme)
        return "{}://{}{}".format(url_parse.scheme, new_netloc, url_parse.path)

    @staticmethod
    def adapt_tlb(url, headers={}):
        if not TLB.is_tlb_task:
            return url, headers
        url_parse = urlparse(url)
        if url_parse.netloc != TLB.get_domain():
            return url, headers

        new_netloc = TLB._get_a_random_ip_port(scheme=url_parse.scheme)
        if headers:
            headers["Host"] = url_parse.netloc
        else:
            headers = {'Host': url_parse.netloc}
        return "{}://{}{}".format(url_parse.scheme, new_netloc, url_parse.path), headers


if __name__ == '__main__':
    print(TLB.adapt_tlb("https://blog.csdn.net/weixin_42902669/article/details/88907704"))
