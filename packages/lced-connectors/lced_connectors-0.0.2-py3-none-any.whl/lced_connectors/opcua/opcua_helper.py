import json
import time

from opcua import ua

from lced_connectors.opcua.opcua_server import OpcuaServer
from lced_utils.buffer_utils import get_connect_info, get_project_connect
from lced_utils.logger_utils import logger


class OpcuaHelper:
    def __init__(self, connect_name=None, tag=None, connect_info=None):
        if connect_info:
            cli_info = connect_info.get(connect_name, {}).get(tag, {})
            self.cli = OpcuaServer(cli_info).get_handler()
            self.uri = cli_info.get("uri")
        else:
            self.cli = get_connect_info().get(connect_name, {}).get(tag)
            self.uri = (
                get_project_connect().get(connect_name, {}).get(tag, {}).get("uri")
            )
        self.attempt = 10
        self.wait_time = 5

    def disconnect(self):
        self.cli.disconnect()
        logger.info("客户端连接已断开")

    def connect(self):
        try:
            self.cli.connect()
        except Exception as e:
            logger.info(f"连接失败: {e}")
        else:
            logger.info("成功连接到 OPC UA 服务器")

    def is_connected(self):
        try:
            self.cli.get_node(ua.NodeId(ua.ObjectIds.Server_ServerStatus)).get_value()
            return True
        except Exception as e:
            logger.info(f"获取opcua节点失败: {e}")
            return False

    def ensure_connection(self):
        if not self.is_connected():
            logger.info("检测到无效连接，重新连接...")
            self.connect()

    def retry_operation(self, operation, *args, **kwargs):
        for _ in range(0, self.attempt):
            try:
                self.ensure_connection()
                return operation(*args, **kwargs)  # 尝试执行操作
            except Exception as e:
                logger.info(f"操作失败: {e}")
                logger.info("重新连接并重试操作...")
                time.sleep(self.wait_time)
        raise ValueError("连接终于断开")

    def device_method_obj(self):
        uri_idx = self.cli.get_namespace_index(self.uri)
        method_obj = self.cli.nodes.root.get_child(["0:Objects", f"{uri_idx}:Device"])
        return method_obj, uri_idx

    def _device_send(self, url, *args):
        method_obj, uri_idx = self.device_method_obj()
        param_list = [ua.NodeId(url, uri_idx)]
        param_list.extend(args)
        res = json.loads(method_obj.call_method(*param_list))
        return res

    def device_send(self, url, *args):
        return self.retry_operation(self._device_send, url, *args)
