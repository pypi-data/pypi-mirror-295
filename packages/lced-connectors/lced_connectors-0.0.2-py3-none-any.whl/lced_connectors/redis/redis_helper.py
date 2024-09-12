from lced_connectors.redis.redis_server import RedisServer
from lced_utils.buffer_utils import get_connect_info


class RedisHelper:
    def __init__(self, connect_name=None, tag=None, connect_info=None):
        if connect_info:
            cli_info = connect_info.get(connect_name, {}).get(tag, {})
            self.cli = RedisServer(cli_info).get_handler()
        else:
            self.cli = get_connect_info().get(connect_name, {}).get(tag)

    def key_del(self, keys):
        self.client.delete(*keys)

    def hash_del(self, key, fields):
        self.client.hdel(key, *fields)

    def client_setname(self, device_id):
        self.client.client_setname(device_id)
        return self.client
