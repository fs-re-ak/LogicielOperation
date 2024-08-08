
from pythonosc import udp_client
import socket
import json
import socket
#from subprocess import check_output # linux


class OSCProxy(object):

    port = None
    configuration = "SENDER"

    def __init__(self, configuration, ip=None, port=10337):
        self.configuration = configuration
        self.port = port
        self.adapter = None

        if ip is None:
            ip = socket.gethostbyname(socket.gethostname())

            # check if a network is available, otherwise hook to local
            if len(ip)<2:
                ip="127.0.0.1"

            ip = ip.split(' ')[0] #if more than one address, select 0 by default

            #reframe for 255
            ip = ip.split('.')[:-1]
            ip.append("255")
            ip = ".".join(ip)
            print(f"OSC-Broadcasting IP: {ip}")


        if self.configuration == "SENDER":
            self.client = udp_client.SimpleUDPClient(ip, port)
            self.client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        else:
            print("[OSCProxy] invalid configuration")

        pass

    def attachAdapter(self, adapter):
        self.adapter = adapter

    def write(self, json_element):
        routes, values = self._process_json(json_element)

        for route, value in zip(routes, values):
            self.client.send_message(route, value)

    def _process_json(self, json_str):
        json_element = json.loads(json_str)
        routes = []
        values = []

        # Extract device_id
        device_id = json_element.get("device_id", "")

        # Convert is_recording to 1 or 0
        status = int(json_element.get("status", 0))
        # Generate route and value for is_recording
        routes.append(f"/{device_id}/status")
        values.append(status)


        # Generate routes and values for metrics
        metrics = json_element.get("metrics", {})
        electrodes = metrics.get("electrodes", {})

        # Cognitive metrics
        for id, value in electrodes.items():
            routes.append(f"/{device_id}/electrodes/{id}/quality")
            values.append(value)

        return routes, values






    def close(self):
        pass
