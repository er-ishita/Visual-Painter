import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

###########################
camheight=720
camwidth=1280

ptime=0
xp,yp=0,0
###########################

cam=cv2.VideoCapture(0)
cam.set(3,camheight)
cam.set(4,camwidth)

detect=htm.HandDetector()

while True:
    succ,img=cam.read()

    if not succ:
        break

    img=cv2.flip(img,1)

    img=detect.findHands(img)
    handlms=detect.findPosition(img)
    fingers=detect.getFingers(handlms)

    print(fingers)

    ctime=time.time()
    fps=int(1/(ctime-ptime))
    ptime=ctime

    cv2.putText(img, f'FPS: {fps}', (10,70),1,cv2.FONT_HERSHEY_COMPLEX,(0,0,255),3)

    cv2.imshow("WebCam",img)
    if cv2.waitKey(1) & 0xff==ord('q'):
        print("Quiting...")
        break

cam.release()
cv2.destroyAllWindows()

