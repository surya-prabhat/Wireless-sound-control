import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.Getmute()
#print(volume.GetMasterVolumeLevel())
#print(volume.GetVolumeRange())



cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            lmlist = []
            for id,lm in enumerate (handlms.landmark):
                h , w, c = img.shape
                cx, cy = int(lm.x*w),int(lm.y*h)
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])
                #print(lmlist)
            mpdraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
        if lmlist:
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1],lmlist[8][2]

            cv2.circle(img,(x1, y1),10,(255,0,9),cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 9), cv2.FILLED)
            cv2.line(img,(x1, y1), (x2, y2),(27,55,130),5)

            length = math.hypot(x2-x1,y2-y1)
            #print(length)

            if length <50:
                z1 = (x1+x2)//2
                z2 = (y1+y2)//2
                cv2.circle(img,(z1, z2) ,10, (255,0,9),cv2.FILLED)

        volrange = volume.GetVolumeRange()
        minvol = volrange[0]
        maxvol = volrange[1]
        vol = np.interp(length, [40,240] ,[minvol,maxvol])
        volbar = np.interp(length ,[50,300] ,[400 ,150])
        volper = np.interp(length ,[50,300] ,[0,100])

        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img ,(50,150) ,(85,400) ,(150,78,240) ,5)
        cv2.rectangle(img ,(50, int(volbar)) ,(85,400) ,(50,58,234) ,cv2.FILLED)
        cv2.putText(img ,str(int(volper)) ,(40,100) ,cv2.FONT_HERSHEY_COMPLEX , 2, (50,58,234))

    cv2.imshow("image",img)
    cv2.waitKey(1)
