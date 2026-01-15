import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import os

###########################
camheight=720
camwidth=1280

brushColor=(255,255,255)

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
            overlay=images[1]
            brushColor=(255,255,255)
        elif(fingers[1] and fingers[2] and fingers[3]==0  and fingers[4]==0):
            x,y=handlms[8][1],handlms[8][2]
            if(x>280 and x<550 and y>0 and y<125):
                overlay=images[3]
                brushColor=(0,0,255)
            ##640-850- blue
            if(x>640 and x<850 and y>0 and y<125):
                overlay=images[0]
                brushColor=(255,0,0)
            #980-1190-  green
            if(x>980 and x<1190 and y>0 and y<125):
                overlay=images[2]
                brushColor=(0,0,255)
        

    ##draw mode
    

    overlay = cv2.resize(overlay, (1280, 125))
    img[0:125,0:1280]=overlay

    cv2.putText(img, f'FPS: {fps}', (10,700),1,cv2.FONT_HERSHEY_COMPLEX,(0,0,255),3)

    cv2.imshow("WebCam",img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        print("Quiting...")
        break

cam.release()
cv2.destroyAllWindows()

