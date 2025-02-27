import json

from umqtt.simple import MQTTClient

class MQTTService:

    def __init__(self, server, user, password, client_id):
        self.user = user
        self.password = password
        self.server = server
        self.subscribe_topic = "msb/state"
        self.client = MQTTClient(client_id, server, user=user, password=password, keepalive=0)
        self.state = None
    def sub_cb(self, topic, msg):
        print("Received message: " + msg.decode())
        data = json.loads(msg.decode())
        self.state = data
        print(data)

    def connect_and_subscribe(self):
        self.client.connect()
        self.client.set_callback(self.sub_cb)
        self.client.subscribe(self.subscribe_topic, qos=0)

    def check_msg(self):
        self.client.check_msg()

    def get_state(self):
        return self.state



