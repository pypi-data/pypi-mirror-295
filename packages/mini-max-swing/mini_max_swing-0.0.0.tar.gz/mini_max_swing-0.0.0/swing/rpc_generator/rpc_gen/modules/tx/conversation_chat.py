import sys
import os
from rpc_generator.core.rpc_driver import RPCDriver
from rpc_generator.core.base_service import BaseService



class ConversationChat(BaseService):
    def __init__(self):
        super().__init__(os.path.abspath(__file__), "data")
        self.psm = "conversation_chat"
        self.service = self.__class__.__name__
        self.business = self.get_dirname(__file__)
        self.branch = "main"
        self.path = os.path.abspath(__file__)  # 当前路径，用于定位配置文件
        self.rpc_driver = RPCDriver(psm=self.psm, service=self.service, business=self.business,
                                    client_path=self.path, data_path=self.data_path, branch=self.branch)

    def AcceptMsg(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def CronJobCallback(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def AcceptStoryMsg(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def AcceptStoryMsgV2(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def AcceptGroupMsg(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def UnifiedAcceptMsg(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def CreateGroupIfNeed(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def SetMsgReply(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def InsertOpenCardAside(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid

    def BatchInsertMsg(self, refresh={}, base=None):
        method = sys._getframe().f_code.co_name
        req = self.get_req_json(method, refresh, base)
        response, logid = self.rpc_driver.rpc_call(req, method)
        return response, logid


if __name__ == "__main__":
    service = ConversationChat("sd://conversation_chat?cluster=default")
