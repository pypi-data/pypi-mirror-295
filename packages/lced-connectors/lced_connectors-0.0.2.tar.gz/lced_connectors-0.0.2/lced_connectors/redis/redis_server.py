import copy
import socket
import redis


class RedisServer:
    def __init__(self, info):
        self.redis_info = copy.deepcopy(info)
        self.redis_info.pop("enable", None)

    def get_handler(self):
        self.redis_info.update(
            {
                "decode_responses": True,
                "retry_on_timeout": True,
                "socket_timeout": 10,
                "socket_connect_timeout": 9,
                "socket_keepalive": True,
                "socket_keepalive_options": {
                    socket.TCP_KEEPIDLE: 120,
                    socket.TCP_KEEPCNT: 2,
                    socket.TCP_KEEPINTVL: 30,
                },
                "health_check_interval": 30,
            }
        )
        r = redis.Redis(**self.redis_info)
        return r
