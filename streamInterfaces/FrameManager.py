


from streamInterfaces.proxies.OSCServerProxy import OSCServerProxy
from streamInterfaces.proxies.UnixSocketProxy import UnixSocketProxy
from streamInterfaces.adapters.FrameAdapter import FrameAdapter

class FrameManager():

    def __init__(self, configuration, deviceFilter="*", stubbed=False):

        self.EmoCogObservers = []

        self.adapter = FrameAdapter(stubbed=stubbed)

        if not stubbed:
            if configuration == "IPC":
                self.proxy = UnixSocketProxy("CLIENT")
                self.proxy.attachAdapter(self.adapter)
            elif configuration == "OSC":
                self.proxy = OSCServerProxy(self.adapter, filter=deviceFilter)
        else:
            self.proxy = None

        pass

    def attachCallback(self, callback):
        self.adapter.addCallback(callback)



