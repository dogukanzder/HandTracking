import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam = 1280, 720


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7, maxHands=10)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]



while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        x3, y3 = lmList[5][1], lmList[5][2]
        x4, y4 = lmList[9][1], lmList[9][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)
        length2 = math.hypot(x4 - x3, y4 - y3)

        if length2 == 0:
            length2 =0.001
        length = math.hypot(x2 - x1, y2 - y1) / length2

        vol = np.interp(length, [0,6], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Image", img)
    cv2.waitKey(1)