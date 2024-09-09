"""
coding:utf-8
@Software: PyCharm
@Time: 2024/6/12 下午9:42
@Author: xingyun
"""
import redis

from rpc_generator.utils.utils import Utils
from rpc_generator.plugins.log.logger import logger


class RedisOp(object):
    def __init__(self, section):
        util = Utils()
        # 创建一个Redis客户端实例
        # 默认连接到本地的Redis服务器，端口为6379
        user = "dataease"
        host = "10.1.32.8"
        port = 6379
        password = "9TAcG1DUFBMzEdrA"
        self.r = redis.Redis(host=host, port=port, db=0, password=password, username=user)

    def test_ping(self):
        # 测试连接
        try:
            # 检查连接是否成功
            pong = self.r.ping()
            if pong:
                print("连接成功！")
        except redis.ConnectionError:
            print("连接失败，请检查Redis服务器是否正在运行。")

    def get_all_keys(self) -> list:
        # 使用SCAN命令获取所有键
        cursor = '0'
        keys = []
        while cursor != 0:
            cursor, data = self.r.scan(cursor=cursor, match='*', count=100)
            keys.extend(data)
            print(keys)
        return keys

    def get_values_string(self, key):
        # 使用GET命令获取键对应的值
        value = self.r.get(key)

        # 检查返回的值是否为None，如果不是None，则打印出来
        if value is not None:
            # print(value.decode('utf-8'))
            return value.decode('utf-8')
            # 如果值是二进制数据，需要解码
        print('Key not found')
        return None

    def del_key(self, key):
        # 使用DEL命令删除键
        # key ='test_key'
        # 如果键存在，DEL命令会返回1，表示成功删除了一个键
        # 如果键不存在，DEL命令会返回0
        deleted_count = self.r.delete(key)
        logger.info(f"Deleted {deleted_count} keys.")

    def del_keys(self, keys):
        # 要删除的多个键
        #  keys = ['my_key1', 'my_key2', 'my_key3']
        # 使用DEL命令删除多个键
        deleted_count = self.r.delete(*keys)
        logger.info(f"Deleted {deleted_count} keys.")

    def set_value(self, key, value, ex=None, exat=None):
        # 要添加的键和值
        # 使用SET命令添加键值对
        self.r.set(key, value)

        # 如果需要设置键的过期时间，可以使用EX或PX参数
        # 例如，设置键在10秒后过期
        # ex = 10
        if ex is not None:
            self.r.set(key, value, ex=ex)
        # 如果需要设置键的过期时间为特定的Unix时间戳，可以使用EXAT参数
        # 例如，设置键在特定时间戳后过期
        if exat is not None:
            # exat = 1686652800  # Unix时间戳
            self.r.set(key, value, exat=exat)

        # 查询是否插入成功
        val = RedisOp(self.session).get_values_string(key)
        if val is not None:
            logger.info('==== set value success ====')
            return True
        logger.info('==== set value fail ====')
        return False


if __name__ == '__main__':
    RedisOp('kaiping_redis').test_ping()
    # RedisOp('kaiping_redis').set_value('test_key', 'test_value')
    # RedisOp('kaiping_redis').get_values_string('cert_data_1793261014549008384')
    RedisOp('kaiping_redis').get_all_keys()
    # db:0 password:ZizMzaIT64Y4exxO path:10.11.16.52:6379 username:xy_test
    # 创建Redis连接对象
    # r = redis.Redis(host='10.11.16.52', port=6379, db=0, password='ZizMzaIT64Y4exxO', username='xy_test')
    # r.get('conversation_repo:cid_cache:162864819228787+56931654476076')
    #
    # # 使用SCAN命令进行模糊查询
    # # 0是初始游标，'user:*'是匹配模式
    # cursor, keys = r.scan(cursor=0, match='conversation_repo:cid_cache:*', count=100)
    #
    # # 遍历返回的键
    # while cursor != 0:
    #     print("Cursor:", cursor)
    #     print("Keys:", keys)
    #     cursor, keys = r.scan(cursor=cursor, match='user:*', count=100)
    #
    # # 如果需要获取这些键的值，可以使用MGET命令
    # values = r.mget(keys)
    # print("Values:", values)

