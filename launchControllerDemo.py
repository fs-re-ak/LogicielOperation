
from time import sleep
from deviceController.DeviceControllerManager import DeviceControllerManager
from streamInterfaces.FrameManager import FrameManager

class Configuration():
    INPUT_FRAME_ACTIVE = False
    DEVICE_CONTROLLER_ACTIVE = False

def frameHandler(frame):
    print("Demo-Frame:" + str(frame))


inputFrames = FrameManager('OSC', stubbed=not Configuration.INPUT_FRAME_ACTIVE)
deviceController = DeviceControllerManager('OSC', stubbed=not Configuration.DEVICE_CONTROLLER_ACTIVE)

inputFrames.attachEmoCogObserver(frameHandler)


"""
sleep(3)
print("Start Recording")
deviceController.sendStartRecording()

for i in range(6):
    deviceController.sendTag("TEST",["Value",i])
    sleep(5)


sleep(1)
deviceController.sendStopRecording()
print("Recording Ended")
sleep(5)

"""

while True:
    sleep(1)
