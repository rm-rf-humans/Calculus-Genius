import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy
import pyautogui

##########################
wCam, hCam = 1360,768
h=640
frameR = 200 
smoothening = 7
#########################

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
plocX,plocY=0,0
clocX,clocY=0,0
detector=htm.handDetector(maxHands=1)
wScr,hScr=autopy.screen.size()

while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmList, bbox= detector.findPosition(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        print(x1, y1, x2, y2)

        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img,(400,100),(wCam-400,h-frameR),(255,0,255),2)

        if fingers[1] == 1 and fingers[2] == 0:
            x3=np.interp(x1,(400,wCam-400),(0,wScr))
            y3=np.interp(y1,(100,h-frameR),(0,hScr))
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            autopy.mouse.move(wScr-clocX,clocY)
            plocX,plocY=clocX,clocY
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)

        if fingers[0] == 0 and fingers[4]==0  or fingers[0]==0 and fingers[4]==1 or fingers[0]==1 and fingers[4]==1 or fingers[0]==1 and fingers[4]==1:
            length,img,lineInfo=detector.findDistance(20,4,img)
            print(length)
            if length<30:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),5,(0,0,255),cv2.FILLED)
                pyautogui.scroll(-15)

        if fingers[0] == 0 and fingers[3]==0  or fingers[0]==0 and fingers[3]==1 or fingers[0]==1 and fingers[3]==1 or fingers[0]==1 and fingers[3]==1:
            length,img,lineInfo=detector.findDistance(16,4,img)
            print(length)
            if length<30:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,0,0),cv2.FILLED)
                pyautogui.scroll(15)

        if fingers[1] == 1 and fingers[2] == 1:
            length,img,lineInfo=detector.findDistance(8,12,img)
            print(length)
            if length<20:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                autopy.mouse.click()

        if fingers[0]==1 and fingers[1]==0:
            cv2.circle(img,(1,1),2,(0,0,0),cv2.FILLED)
            pyautogui.click(button='middle')

        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] ==0:
            length,img,lineInfo=detector.findDistance(4,8,img)
            print(length)
            if length<15:
                exit()
        

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow('Image',img)
    cv2.waitKey(1)
    
