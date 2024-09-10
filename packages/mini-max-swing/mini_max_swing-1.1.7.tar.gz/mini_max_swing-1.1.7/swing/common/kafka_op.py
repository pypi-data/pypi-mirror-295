"""
coding:utf-8
@Software: PyCharm
@Time: 2024/7/9 下午7:18
@Author: xingyun
"""
from kafka import KafkaProducer, KafkaConsumer
from swing.rpc_generator.utils.utils import Utils
from swing.rpc_generator.plugins.log.logger import logger


class KafkaOp(object):
    def __init__(self, section, topic=None, group_id=None):
        util = Utils()
        # 创建一个Redis客户端实例
        # 默认连接到本地的Redis服务器，端口为6379
        # user = util.get_conf('kaiping_redis', 'user')
        host = util.get_git_conf(section, 'host')
        port = int(util.get_git_conf(section, 'port'))
        console = util.get_git_conf(section, 'console')
        # 创建一个 Kafka 生产者实例
        self.producer = KafkaProducer(bootstrap_servers=[f'{host}:{port}'],
                                      value_serializer=lambda v: v.encode('utf-8'))
        # 创建一个 Kafka 消费者实例
        if topic is not None and group_id is not None:
            self.consumer = KafkaConsumer(topic,
                                          bootstrap_servers=[f'{host}:{port}'],
                                          auto_offset_reset='earliest',
                                          enable_auto_commit=True,
                                          group_id=group_id)

    # Kafka 生产者示例
    def produce_messages(self):
        # 发送消息
        for i in range(10):
            self.producer.send('your_topic', f'Message {i}'.encode('utf-8'))
            self.producer.flush()  # 确保所有消息都被发送

        logger.info("Messages sent successfully.")

    # Kafka 消费者示例
    def consume_messages(self):
        for message in self.consumer:
            logger.info(f"Received message: {message.value.decode('utf-8')}")
