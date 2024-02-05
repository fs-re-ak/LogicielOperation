
from time import sleep
from deviceController.DeviceControllerManager import DeviceControllerManager
from streamInterfaces.FrameManager import FrameManager
from random import shuffle, seed
import winsound

frequency = 200  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second


def generateBalancedRandomizedTrialSequence(nbClasses, nbOfPresentation, SEED=None):
    trialSequence = []

    if SEED is not None:
        seed(SEED)

    for i in range(nbOfPresentation):
        subSequence = [i for i in range(nbClasses)]
        shuffle(subSequence)

        # if last element of sequence is same as first of sequence extension
        # permute the first two of sequence extension
        if len(trialSequence) > 0:
            if trialSequence[-1] == subSequence[0]:
                tmp = subSequence[0]
                subSequence[0] = subSequence[1]
                subSequence[1] = tmp

        trialSequence += subSequence

    return trialSequence


class Configuration():
    INPUT_FRAME_ACTIVE = True
    DEVICE_CONTROLLER_ACTIVE = True

def frameHandler(frame):
    #print("Demo-Frame:" + str(frame))
    pass



#Configure objects
inputFrames = FrameManager('OSC', stubbed=not Configuration.INPUT_FRAME_ACTIVE)
deviceController = DeviceControllerManager('OSC', stubbed=not Configuration.DEVICE_CONTROLLER_ACTIVE)
inputFrames.attachEmoCogObserver(frameHandler)

# prepare experiments paramters
EXPRESSIONS = ["NEUTRAL", "HAPPY", "ANGER", "BLINKS", "JAW_CLENCH", "LOOK_LEFT", "LOOK_RIGHT"]
NB_PRESENTATIONS = 3
PREPARE_DELAY = 3
MAINTAIN_DELAY = 6

trialsSequence = generateBalancedRandomizedTrialSequence(len(EXPRESSIONS), NB_PRESENTATIONS)



sleep(3)
print("Beginning of the experiment")
deviceController.sendStartRecording()
sleep(3)
deviceController.sendTag("BASELINE",str(["BASELINE"]))
print("Maintain - Neutral, for baseline")
sleep(10)

for idx, stimuliId in enumerate(trialsSequence):
    if EXPRESSIONS[stimuliId] != "BLINKS":
        print(f"Prepare for this expression: {EXPRESSIONS[stimuliId]}")
        print(f"Maintain from beep to beep")
        sleep(PREPARE_DELAY-duration/1000)
        deviceController.sendTag("TRIAL",str([idx, EXPRESSIONS[stimuliId]]))
        winsound.Beep(frequency,duration)
        sleep(MAINTAIN_DELAY-duration/1000)
        winsound.Beep(frequency,duration)
    elif EXPRESSIONS[stimuliId] == "BLINKS":
        print(f"Blink at every beep")
        sleep(PREPARE_DELAY-duration/1000)
        for i in range(MAINTAIN_DELAY):
            deviceController.sendTag("TRIAL",str([idx, EXPRESSIONS[stimuliId]]))
            winsound.Beep(frequency,duration)
            sleep(1)

sleep(1)
deviceController.sendStopRecording()
print("End of the experiment")
sleep(5)
