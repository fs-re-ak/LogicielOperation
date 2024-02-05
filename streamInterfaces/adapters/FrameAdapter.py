
import json
from threading import Thread
from time import sleep
import random

class FrameAdapter():

    def __init__(self, stubbed=False):

        self.manager = None

        if stubbed:
            fakeDataThread = Thread(target=self.fakeDataTask)
            fakeDataThread.daemon = True
            fakeDataThread.start()

        pass


    def fakeDataTask(self):

        while True:
            unpackedFrame = {"Neutral": random.random(), "Happiness": random.random(), "Anger": random.random(), "Engagement": random.random()*1.5}
            if self.manager is not None:
                #print("[FrameAdapter] Stubbed")
                self.manager.frameUnpacked(unpackedFrame)
            else:
                print(unpackedFrame)
            sleep(0.5)

    def attachManager(self, manager):
        self.manager = manager
        pass


    def msgCallback(self, frame):

        # unpack context and return results
        frame = json.loads(frame)
        
        if "Metrics" not in frame.keys():
            return 
        
        unpackedFrame = {"Neutral": frame["Metrics"]["Emotions"][0], "Happiness": frame["Metrics"]["Emotions"][1], "Anger": frame["Metrics"]["Emotions"][2], "Engagement": frame["Metrics"]["Engagement"][0]}
        
        if self.manager is not None:
            self.manager.frameUnpacked(unpackedFrame)
        else:
            print(unpackedFrame)
        pass
