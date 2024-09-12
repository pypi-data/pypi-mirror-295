import json

from lced_connectors.mqtt.mqtt_server import MqttServer
from lced_utils.buffer_utils import get_connect_info
from lced_utils.logger_utils import logger


class MqttHelper:
    def __init__(self, connect_name=None, tag=None, connect_info=None):
        if connect_info:
            cli_info = connect_info.get(connect_name, {}).get(tag, {})
            self.cli = MqttServer(cli_info).get_handler()
        else:
            self.cli = get_connect_info().get(connect_name, {}).get(tag)

    def publish_message(self, topic, payload, qos=2, retain=False):
        p_payload = json.dumps(payload, ensure_ascii=False)
        self.cli.publish(topic, p_payload, qos=qos, retain=retain)
        logger.info(
            f"Mqtt Sending info include <topic:{topic}, payload:{p_payload}, qos:{qos}, retain:{retain}>"
        )
