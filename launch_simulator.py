
from time import sleep

from simulator.FrameStream import FrameStreamAdapter

from simulator.proxy.OSCProxy import OSCProxy



def launchSimulation():

    stream = FrameStreamAdapter(deviceId="reak-hermes-5")
    proxy = OSCProxy("SENDER")
    stream.attachProxy(proxy)

    stream.setStatus("READY")


    electrodePackage = {
        "1":0,
        "2":1,
        "3":0,
        "4":1,
        "5":0,
        "6":1,
        "7":0,
        "8":1,
        "100":0
    }

    stream.addMetricsKeyValue("electrodes", electrodePackage)

    stream.startStream()


    while(True):
        sleep(1)










if __name__ == "__main__":
    launchSimulation()