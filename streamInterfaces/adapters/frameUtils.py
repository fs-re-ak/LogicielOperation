
import random


def createFrame():

    frame = {"engagement":0,
             "anger":0,
             "contempt":0,
             "disgust":0,
             "fear":0,
             "happiness":0,
             "neutral":0,
             "sadness":0,
             "surprise":0
             }

    return frame




def assignRandomValues(frame):

    for k in frame.keys():
        frame[k] = random.random()



def showFrame(frame):

    for k,v in frame.items():
        print(f"{k} : {v*100:.2f}, ", end='')

    print()







