


from streamInterfaces.proxies.OSCServerProxy import OSCServerProxy
from streamInterfaces.proxies.UnixSocketProxy import UnixSocketProxy
from streamInterfaces.adapters.FrameAdapter import FrameAdapter

class FrameManager():

    def __init__(self, configuration, stubbed=False):

        self.EmoCogObservers = []

        self.adapter = FrameAdapter(stubbed=stubbed)

        if not stubbed:
            if configuration == "IPC":
                self.proxy = UnixSocketProxy("CLIENT")
                self.proxy.attachAdapter(self.adapter)
            elif configuration == "OSC":
                self.proxy = OSCServerProxy(self.adapter)
        else:
            self.proxy = None

        self.adapter.attachManager(self)

        pass

    def attachEmoCogObserver(self, handle):
        self.EmoCogObservers.append(handle)

    def frameUnpacked(self, dataSample):
        # connect with experience monitoring
        for handle in self.EmoCogObservers:
            handle(dataSample)



