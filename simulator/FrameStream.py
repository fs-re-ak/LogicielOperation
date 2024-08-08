import json
import uuid
from datetime import datetime
from threading import Lock, Thread
from time import time, sleep
import copy
from simulator.FrameDefinition import Frame


class FrameStreamAdapter():
    cognitive = None
    emotional = None
    powerBands = None
    serialNumber = None

    frameLock = None

    active = True
    alwaysActive = False

    sendFramesThread = None

    period = None

    manager = None
    proxy = None
    streamType = None

    count = 0

    def __init__(self, period=0.5, deviceId=None):
        self.frameLock = Lock()
        self.period = period
        self.deviceId = deviceId
        self.count = 0
        self.status = 0
        self.active = False

        self.metrics = {}

        self.sendFramesThread = Thread(target=self.sendFrameTask)
        self.sendFramesThread.daemon = True
        self.sendFramesThread.start()
        pass

    def attachProxy(self, proxy):
        self.proxy = proxy

    def startStream(self):
        self.count = 0
        self.active = True
        pass

    def stopStream(self):
        self.active = False
        pass


    def setStatus(self, status):

        if status=="UNKNOWN":
            self.status = 0
        elif status=="BUSY":
            self.status = 1
        elif status=="READY":
            self.status = 2
        elif status=="RECORDING":
            self.status = 3
        pass


    def addMetricsKeyValue(self, key: str, value):
        self.frameLock.acquire()
        self.metrics[key] = copy.deepcopy(value)
        self.frameLock.release()
        pass

    def removeMetricsKey(self, key: str):
        self.metrics.pop(key, None)

    def sendFrameTask(self):

        while True:

            startTime = time()
            if self.active:

                # copy values
                self.frameLock.acquire()

                metrics = copy.deepcopy(self.metrics)

                # build frame
                frame = Frame(count=self.count, status=self.status, device_id=self.deviceId, **metrics)
                self.count += 1

                # send frame
                if self.proxy is not None:

                    frame_str = str(frame.toJSON().replace("\n", " ").replace(" ", ""))
                    try:
                        self.proxy.write(frame_str)
                    except:
                        pass
                self.frameLock.release()

            # wait
            sleeptime = self.period - (time() - startTime)
            sleep(sleeptime if sleeptime > 0 else 0)

        pass
