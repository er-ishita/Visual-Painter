import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self,mode=False,maxHands=2,detCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detCon=detCon
        self.trackCon=trackCon

        self.mpHand=mp.solutions.hands
        self.hand=self.mpHand.Hands()
        self.mpDraw=mp.solutions.drawing_utils

        self.results=None

    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hand.process(imgRGB)
        if self.results and self.results.multi_hand_landmarks:
            for lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,lms,self.mpHand.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        handLms=[]

        if self.results and self.results.multi_hand_landmarks:
            hand=self.results.multi_hand_landmarks[handNo]
            h,w,_=img.shape
            for id,lm in enumerate(hand.landmark):
                cx,cy=int(lm.x*w),int(lm.y*h)
                if draw:
                    cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
                handLms.append([id,cx,cy])

        return handLms
    
    def getFingers(self,handlms):
        fingers=[]

        if len(handlms)>=21:
            if(handlms[4][1]<handlms[3][1]):
                fingers.append(1)
            else:
                fingers.append(0)
            
            fing=[8,12,16,20]
            for i in fing:
                if(handlms[i][2]<handlms[i-2][2]):
                    fingers.append(1)
                else:
                    fingers.append(0)
            
        return fingers
        
def main():
    cam=cv2.VideoCapture(0)
    ptime=0
    htm=HandDetector()

    while True:
        succ, img=cam.read()
        if not succ:
            break

        img=cv2.flip(img, 1)
        img=htm.findHands(img)
        handlms=htm.findPosition(img)
        fingers=htm.getFingers(handlms)
        
        if len(fingers)!=0:
            print(fingers)

        ctime=time.time()
        fps=int(1/(ctime-ptime))
        ptime=ctime

        # if len(handlms)!=0:
        #     print(handlms[4])

        cv2.putText(img,f'FPS: {fps}',(10,70),1,cv2.FONT_HERSHEY_COMPLEX_SMALL,(0,0,255),3)

        cv2.imshow("Webcam",img)

        if cv2.waitKey(1) & 0xff==ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()