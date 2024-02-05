
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from typing import List, Any
from threading import Thread

class OSCServerProxy():

    def __init__(self, adapter):
        self.dispatcher = Dispatcher()
        self.adapter = adapter
        self.dispatcher.map("/*", self._set_filter)  # Map wildcard address to set_filter function
        self.server = BlockingOSCUDPServer(("0.0.0.0", 10337), self.dispatcher)

        self.servingThread = Thread(target=self._servingTask)
        self.servingThread.daemon = True
        self.servingThread.start()

        pass

    def _servingTask(self):
        while True:
            self.server.handle_request()

    def _set_filter(self, address: str, *args: List[Any]) -> None:
        self.adapter.msgCallback(args[0])

    def disconnect(self):
        pass

