import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import os
import numpy as np

###########################
camheight=720
camwidth=1280

brushColor=(0,0,0)
brushThickness = 25
eraserThickness = 100

canvas = np.zeros((720, 1280, 3), np.uint8)

ptime=0
xp,yp=0,0
###########################

cam=cv2.VideoCapture(0)
cam.set(3, camwidth)
cam.set(4, camheight)


detect=htm.HandDetector()

images=[]

for sm in os.listdir("Visual-Painter/images"):
    im=cv2.imread(f'Visual-Painter/images/{sm}')
    images.append(im)

# print(images)

overlay=images[1]

while True:
    succ,img=cam.read()

    if not succ:
        break

    img=cv2.flip(img,1)

    fingers=[]

    img=detect.findHands(img)
    handlms=detect.findPosition(img)
    if len(handlms)!=0:
        fingers=detect.getFingers(handlms)
    
    # if len(handlms)>8:
    #     print(handlms[8])

    # print(fingers)

    ctime=time.time()
    fps=int(1/(ctime-ptime))
    ptime=ctime

    ##selection mode
    if len(fingers)!=0:
        if (fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]):
            xp,yp=0,0
            overlay=images[1]
            brushColor=(0,0,0)
        elif(fingers[1] and fingers[2] and fingers[3]==0  and fingers[4]==0):
            x,y=handlms[8][1],handlms[8][2]
            x2, y2 = handlms[12][1:]
            if(x>280 and x<550 and y>0 and y<125):
                overlay=images[3]
                brushColor=(0,0,255)
            ##640-850- blue
            if(x>640 and x<850 and y>0 and y<125):
                overlay=images[0]
                brushColor=(255,100,0)
            #980-1190-  green
            if(x>980 and x<1190 and y>0 and y<125):
                overlay=images[2]
                brushColor=(0,255,0)
            cv2.rectangle(img, (x, y-25), (x2, y2 + 25), brushColor, cv2.FILLED)        
    
    ##draw mode
    if len(fingers)!=0:
        if ((fingers[0]==0) and fingers[1] and (fingers[2]==0) and (fingers[3]==0) and (fingers[4]==0)):
            x,y=handlms[8][1],handlms[8][2]
            cv2.circle(img, (x, y), 30, brushColor, cv2.FILLED)
            if xp == 0 or yp == 0:
                xp, yp = x, y
            if(brushColor==(0,0,0)):
                cv2.line(canvas, (xp, yp), (x, y), brushColor, eraserThickness)
            else:
                cv2.line(canvas, (xp, yp), (x, y), brushColor, brushThickness)
            xp,yp=x,y
        else:
            xp,yp=0,0
    

    imgGray=cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
    _,imInverse=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imInverse=cv2.cvtColor(imInverse,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imInverse)
    img=cv2.bitwise_or(img,canvas)

    overlay = cv2.resize(overlay, (1280, 125))
    img[0:125,0:1280]=overlay

    cv2.putText(img, f'FPS: {fps}', (10,700),1,cv2.FONT_HERSHEY_COMPLEX,(0,0,255),3)

    cv2.imshow("WebCam",img)
    # cv2.imshow("Canvas",canvas)
    if cv2.waitKey(1) & 0xff==ord('q'):
        print("Quiting...")
        break

cam.release()
cv2.destroyAllWindows()

