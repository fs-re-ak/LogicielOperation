
import json
from threading import Thread
from time import sleep, time
import random

from streamInterfaces.adapters.frameUtils import createFrame, assignRandomValues

class FrameAdapter():

    def __init__(self, stubbed=False):

        self.manager = None
        self.frame = createFrame()
        self.callbacks = []
        self.stubbed = stubbed

        periodicCallbackThread = Thread(target=self.periodicCallbackTask)
        periodicCallbackThread.daemon = True
        periodicCallbackThread.start()

        pass


    def periodicCallbackTask(self):

        while True:

            if self.stubbed:
                assignRandomValues(self.frame)

            for callback in self.callbacks:
                callback(self.frame)

            sleep(0.5)

    def addCallback(self,callback):
        self.callbacks.append(callback)

    def msgCallback(self, address, message):

        metric = address.split('/')[-1]

        if metric in self.frame.keys():
            self.frame[metric] = float(message)

        pass
