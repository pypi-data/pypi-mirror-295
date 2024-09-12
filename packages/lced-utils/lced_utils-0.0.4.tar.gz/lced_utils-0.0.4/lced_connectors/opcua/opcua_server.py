import copy
import logging
from opcua import Client

from lced_utils.url_utils import format_base_url


class OpcuaServer:
    def __init__(self, info):
        self.opcua_info = copy.deepcopy(info)
        self.opcua_info.pop("enable", None)
        self.timeout = self.opcua_info["timeout"]

    def get_handler(self):
        client = Client(format_base_url(self.opcua_info), self.timeout)
        # 设置超时时间
        client.secure_channel_timeout = 10 * 60 * 1000
        client.session_timeout = 10 * 60 * 1000
        # 关闭日志打印
        op_logger = logging.getLogger("opcua.uaprotocol")
        op_logger.setLevel(logging.WARNING)
        op_logger = logging.getLogger("opcua.client.ua_client")
        op_logger.setLevel(logging.WARNING)
        client.connect()
        return client
