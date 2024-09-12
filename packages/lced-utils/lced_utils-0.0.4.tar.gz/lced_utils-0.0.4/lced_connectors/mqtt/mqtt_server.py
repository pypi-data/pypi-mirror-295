import copy

import paho.mqtt.client as mqtt

from lced_utils.uuid_utils import generate_uuid4


class MqttServer:
    def __init__(self, info):
        self.mqtt_info = copy.deepcopy(info)
        self.mqtt_info.pop("enable", None)
        self.username = self.mqtt_info.pop("username", None)
        self.password = self.mqtt_info.pop("password", None)

    def get_handler(self):
        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=generate_uuid4(),
            protocol=mqtt.MQTTProtocolVersion.MQTTv311,
        )
        if self.username and self.password:
            client.username_pw_set(self.username, self.password)
        client.connect(**self.mqtt_info)
        return client
