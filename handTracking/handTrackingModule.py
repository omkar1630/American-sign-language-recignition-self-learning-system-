import math

import cv2
import mediapipe as mp
import streamlit
import numpy
import tempfile
import time
from PIL import Image

class HandDetector():
    def __init__(self,mode=False,maxHands=2,model_complexity=1,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelCompatibility=model_complexity
        self.detectionCon=min_detection_confidence
        self.trackingCon=min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelCompatibility,
                                        self.detectionCon,self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils

        # self.lmlist = []
        self.condition=True

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.lmlist=[]
        if (self.results.multi_hand_landmarks):
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(handNo)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    if id == 0 or id == 4 or id == 8 or id == 12 or id == 16 or id == 20:
                        cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
        return self.lmlist

    def signCondition(self):
        # fingers = []
        # if self.lmlist:
        #     fingers.append(1 if self.lmlist[4][2] < self.lmlist[3][2] else 0)    # thumb
        #     fingers.append(1 if self.lmlist[8][2] < self.lmlist[6][2] else 0)    # index
        #     fingers.append(1 if self.lmlist[12][2] < self.lmlist[10][2] else 0)  # middle
        #     fingers.append(1 if self.lmlist[16][2] < self.lmlist[14][2] else 0)  # ring
        #     fingers.append(1 if self.lmlist[20][2] < self.lmlist[18][2] else 0)  # pinky

        #     if fingers == [0,0,0,0,0]:
        #         return '0'
        #     elif fingers == [0,1,0,0,0]:
        #         return '1'
        #     elif fingers == [0,1,1,0,0]:
        #         return '2'
        #     elif fingers == [0,1,1,1,0]:
        #         return '3'
        #     elif fingers == [0,1,1,1,1]:
        #         return '4'
        #     elif fingers == [1,1,1,1,1]:
        #         return '5'
        #     elif fingers == [1,0,0,0,1]:
        #         return '6'
        #     elif fingers == [1,1,0,0,1]:
        #         return '7'
        #     elif fingers == [1,0,1,0,1]:
        #         return '8'
        #     elif fingers == [1,0,0,1,1]:
        #         return '9'

        # ✅ Your alphabet detection block
        if self.lmlist[8][2] < self.lmlist[6][2] and self.lmlist[12][2] > self.lmlist[10][2] and self.lmlist[16][2] > self.lmlist[14][2] and self.lmlist[20][2] > self.lmlist[18][2]:
            if self.lmlist[4][1] > self.lmlist[8][1]:
                return "l"
            elif self.lmlist[4][2] >= self.lmlist[12][2]:
                return "d"
            elif self.lmlist[4][2] < self.lmlist[12][2]:
                if (self.lmlist[6][2] - self.lmlist[7][2]) > (-15) and (self.lmlist[6][2] - self.lmlist[7][2]) < 15:
                    return "x"
                else:
                    return "z"
            else:
                return "else"
        elif self.lmlist[8][2] > self.lmlist[6][2] and self.lmlist[12][2] > self.lmlist[10][2] and self.lmlist[16][2] > self.lmlist[14][2] and self.lmlist[20][2] > self.lmlist[18][2]:
            if self.lmlist[4][1] > self.lmlist[8][1] and self.lmlist[4][2] < self.lmlist[8][2]:
                return "a"
            elif (self.lmlist[8][1] > self.lmlist[0][1] and self.lmlist[12][1] > self.lmlist[0][1] and self.lmlist[16][1] > self.lmlist[0][1] and self.lmlist[20][1] > self.lmlist[0][1]) and (self.lmlist[3][2] - self.lmlist[8][2]) >= 50:
                return "c"
            elif (self.lmlist[4][2] > self.lmlist[17][2]) and self.lmlist[4][2] >= self.lmlist[8][2] and self.lmlist[3][2] > self.lmlist[8][2] and self.lmlist[3][2] < self.lmlist[4][2]:
                return "e"
            elif (self.lmlist[4][1] > self.lmlist[18][1]) and (self.lmlist[4][1] < self.lmlist[14][1]):
                return "m"
            elif (self.lmlist[4][1] > self.lmlist[14][1]) and (self.lmlist[4][1] < self.lmlist[10][1]):
                if (self.lmlist[4][2] > self.lmlist[10][2] and self.lmlist[4][2] < self.lmlist[8][2]):
                    return "s"
                else:
                    return "n"
            elif (self.lmlist[4][1] > self.lmlist[10][1]) and (self.lmlist[4][1] < self.lmlist[6][1] and self.lmlist[4][2] < self.lmlist[8][2]):
                return "t"
            elif self.lmlist[8][1] < self.lmlist[6][1] and self.lmlist[4][1] < self.lmlist[2][1] and self.lmlist[12][1] < self.lmlist[10][1] and self.lmlist[16][1] < self.lmlist[14][1] and self.lmlist[20][1] < self.lmlist[18][1] and ((self.lmlist[4][1] - self.lmlist[8][1] <= 10 and self.lmlist[4][1] - self.lmlist[8][1] >= (-10)) or (self.lmlist[4][2] - self.lmlist[8][2] <= 10 and self.lmlist[4][2] - self.lmlist[8][2] >= (-10))):
                return "o"
            else:
                return "else"
        elif(self.lmlist[8][2] < self.lmlist[6][2] and self.lmlist[12][2] < self.lmlist[10][2] and self.lmlist[16][2] < self.lmlist[14][2] and self.lmlist[20][2] < self.lmlist[18][2] and self.lmlist[4][1]<self.lmlist[5][1]):
            return "b"
        elif self.lmlist[12][2] < self.lmlist[10][2] and self.lmlist[16][2] < self.lmlist[14][2] and self.lmlist[20][2] < self.lmlist[18][2] and ((self.lmlist[4][1]-self.lmlist[8][1]<=10 and self.lmlist[4][1]-self.lmlist[8][1]>=(-10)) or (self.lmlist[4][2]-self.lmlist[8][2]<=10 and self.lmlist[4][2]-self.lmlist[8][2]>=(-10))):
                return "f"
        elif self.lmlist[8][1]<self.lmlist[6][1] and self.lmlist[4][1]<self.lmlist[3][1] and self.lmlist[12][1]>self.lmlist[10][1] and self.lmlist[16][1]>self.lmlist[14][1] and self.lmlist[20][1]>self.lmlist[18][1]:
                if self.lmlist[4][2]>self.lmlist[10][2]:
                    return "q"
                else:
                    return "g"
        elif self.lmlist[8][1]<self.lmlist[6][1] and self.lmlist[4][1]<self.lmlist[3][1] and self.lmlist[12][1]<self.lmlist[10][1] and self.lmlist[16][1]>self.lmlist[14][1] and self.lmlist[20][1]>self.lmlist[18][1]:
                if self.lmlist[12][2]<self.lmlist[4][2]:
                    return "h"
                else:
                    return "p"
        elif(self.lmlist[20][2]<self.lmlist[18][2] and self.lmlist[16][2]>self.lmlist[14][2] and self.lmlist[12][2]>self.lmlist[10][2] and self.lmlist[8][2]>self.lmlist[6][2] and self.lmlist[4][1]<self.lmlist[3][1]):
                return "i"
        elif (self.lmlist[20][2] > self.lmlist[18][2] and self.lmlist[16][2] < self.lmlist[14][2] and self.lmlist[12][2] < self.lmlist[10][2] and self.lmlist[8][2] < self.lmlist[6][2] and self.lmlist[4][1] < self.lmlist[3][1]):
                if self.lmlist[20][2]>self.lmlist[0][2]:
                    return "j"
                elif self.lmlist[20][2]<self.lmlist[0][2]:
                    return "w"
        elif self.lmlist[20][2] > self.lmlist[18][2] and self.lmlist[16][2] > self.lmlist[14][2] and self.lmlist[12][2] < self.lmlist[10][2] and self.lmlist[8][2] < self.lmlist[6][2]:
                if self.lmlist[4][1] < self.lmlist[6][1] and self.lmlist[4][1] > self.lmlist[10][1]:
                    return "k"
                else:
                    if self.lmlist[8][1] - self.lmlist[12][1]>(-30) and self.lmlist[8][1] - self.lmlist[12][1]<30:
                        if self.lmlist[8][1]<self.lmlist[12][1]:
                            return "r"
                        else:
                            return "u"
                    else:
                        return "v"
        elif self.lmlist[16][2] > self.lmlist[14][2] and self.lmlist[12][2] > self.lmlist[10][2] and self.lmlist[8][2] > self.lmlist[6][2] and self.lmlist[20][2] < self.lmlist[18][2]:
                return "y"
        elif self.lmlist[8][1]<=10 and self.lmlist[8][1]>=(-10):
                self.condition=False           #closing the windows condition
                return "else"
        else:
            return"else"
            


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector=HandDetector()
    while True:

        success, img = cap.read()
        img=detector.findHands(img,draw=True)  #we can make it true or false
        # detector.findPosition(img)
        lmlist=detector.findPosition(img,draw=True)
        if len(lmlist)!=0:
            print(lmlist[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3
                    , (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()