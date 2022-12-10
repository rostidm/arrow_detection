import cv2
import math
import numpy as np


def getcontours(vdo,th):
    contours, hierarchy= cv2.findContours(vdo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for ix, contour in enumerate(contours):
         area= cv2.contourArea(contour)

         if area>1000:
             cv2.drawContours(th, contours, -1, (0,255,0), 3)
             peri=cv2.arcLength(contour, True)
             approx=cv2.approxPolyDP(contour, 0.02*peri, True)
             objcor=len(approx)
             x, y, w, h = cv2.boundingRect(approx)

             if objcor ==7:
                 startpoint= (approx[0][0][0],approx[0][0][1])
                 endpoint=(int((approx[3][0][0]+approx[4][0][0])/2),int((approx[3][0][1]+approx[4][0][1])/2))
                 angle= math.degrees(math.atan2(endpoint[1]-startpoint[1], endpoint[0]-startpoint[0]))
                 if angle < 0:
                     angle += 360

                 print('angle=', angle)
             else:
                 pass
    
cap=cv2.VideoCapture(0)

while True:
    _, frame= cap.read()
    blur=cv2.GaussianBlur(frame, (5,5), 0)
    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    lower_red=np.array([0,100,100])
    upper_red=np.array([10,255,255])
    mask=cv2.inRange(hsv,lower_red, upper_red)

    result= cv2.bitwise_and(frame, frame, mask=mask)

    ab,th=cv2.threshold(result, 133,255, cv2.THRESH_BINARY)
    th1=cv2.erode(th,None, iterations=2)
    th1=cv2.dilate(th, None, iterations=2)

    getcontours(mask,th1)

    cv2.imshow('th', th)
    cv2.imshow("frame", frame)

    key= cv2.waitKey(500)
    
    if key== 27:
        break

cap.release()
cv2.destroyAllWindows()