
from pythonosc import udp_client
import socket

class OSCClientProxy(object):

    port = None

    def __init__(self, ip="192.168.191.255", port=10338):
        self.port = port
        self.adapter = None

        print(ip)

        self.client = udp_client.SimpleUDPClient(ip, port)
        self.client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        pass

    def attachAdapter(self, adapter):
        self.adapter = adapter

    def write(self, msg, route="/control"):
        self.client.send_message(route, msg)

    def close(self):
        pass
