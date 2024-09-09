import pytest
from modules.tx.conversation_chat import ConversationChat
from common.common import Common


class TestConversationChat(object):
    def test_AcceptStoryMsgV2(self):
        """
        用例描述：测试 AcceptStoryMsgV2 接口正常情况
        """
        caseparam = {
            "env": "all",
            "rpc_method": ConversationChat().AcceptStoryMsgV2,
            "rpc_param": {
                "xxx你的参数填在这里xxxx": ""
            },
            "expect": {
                "stcAssertPart": {
                    "xxxx 你的结果断言写在这里": ""
                }
            },
            # 不需要日志断言 可以去掉
            "log_assert": {
                "xxxx 你的日志断言写在这里": ""
            }
        }
        Common.api_handle(caseparam)       

