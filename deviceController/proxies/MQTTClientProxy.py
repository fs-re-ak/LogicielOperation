
import os
import socket
from pythonosc import udp_client

import paho.mqtt.client as mqtt
from threading import Thread
from time import sleep


class MQTTClientProxy():

    def __init__(self, host='localhost', port=1883, routes = []):

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self._on_connect
        self.mqttc.on_disconnect = self._on_disconnect
        self.mqttc.on_message = self._on_message
        self.routes = routes
        #self.host = host
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port

        # non blocking, handles reconnect
        self.mqttc.loop_start()

        self.thread = Thread(target=self._connectTask)
        self.thread.daemon = True
        self.thread.start()

    def attachAdapter(self, adapter):
        self.adapter = adapter

    def _connectTask(self):
        self.connected = False

        while not self.connected:
            try:
                self.mqttc.connect(self.host, self.port, 60)
                self.connected = True
            except:
                print("MQTT - connection failed, retrying")
                pass


    # The callback for when the client receives a CONNACK response from the server.
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")

        for route in self.routes:
            client.subscribe(route)

    def _on_disconnect(self, Client, userdata, flags, reason_code, properties):
        print(f"Disconnected with result code {reason_code}")

        self.thread = Thread(target=self._connectTask)
        self.thread.daemon = True
        self.thread.start()

    # The callback for when a PUBLISH message is received from the server.
    def _on_message(self, client, userdata, msg):
        if self.adapter is not None:
            self.adapter.decode(msg.topic + " " + str(msg.payload))

    def write(self, msg, route="control/"):
        if self.connected:
            print(msg)
            try:
                self.mqttc.publish(route, msg)
            except:
                print("[MQTTClientProxy.py] Error sending")
                pass
        else:
            print("[MQTTClientProxy.py] Trying to send, when not connected")

    def close(self):
        self.mqttc.disconnect()




if __name__ == "__main__":
    class Adapter():
        def decode(self, msg):
            print(msg)

    proxy = MQTTClientProxy(host="192.168.50.202")
    adapter = Adapter()

    proxy.attachAdapter(adapter)

    sleep(3)
    proxy.write("control/","Hello")

    sleep(200)