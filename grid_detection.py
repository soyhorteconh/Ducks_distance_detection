#!/usr/bin/env python

# Importing Librariesimport cv2
#from curses import window
import cv2
import numpy as np
from matplotlib import pyplot as plt





#Capturing video
cap = cv2.VideoCapture("patitos.mp4")

while True: 
    _,frame = cap.read()

    blurred = cv2.GaussianBlur(frame, (15, 15), 0, None)
    dst = cv2.fastNlMeansDenoisingColored(blurred,None,6,6,1,1)
    #cv2.imshow("dst", dst)

    image = cv2.cvtColor(dst,cv2.COLOR_BGR2HLS)
    #image = cv2.cvtColor(blurred,cv2.COLOR_Lab2RGB)
    #image = cv2.cvtColor(blurred,cv2.COLOR_RGB2GRAY)
    #cv2.imshow("video", image)
    
    lower = np.uint8([0, 200, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    # yellow color mask
    lower = np.uint8([10, 0,   100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    #cv2.imshow("mask",mask)

    blurred = cv2.GaussianBlur(mask, (15, 15), 0, None)
    #cv2.imshow("blurred", blurred) 

    canny = cv2.Canny(blurred, 0, 255)

    cv2.imshow('window', canny)

    #detect contours
    cnts, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    prom_l = 0

    for cnt in cnts:
        x1,y1 = cnt[0][0]
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        #print(len(approx))

        if (len(approx) == 5):
            # x y son coordendas
            x, y, w, h = cv2.boundingRect(cnt)

            perimeter = 2* (w + h) 
            l = perimeter / 4
            
            if(l > 50 and l < 200):
                print("lado: ", l)
                print("altura: ", h)
                print("ancho: ", w)
                
                dif = h-w
                print(dif)

                if (dif < 90 and dif > -90):
                    print(dif)
                    img = cv2.drawContours(dst, [cnt], -1, (0,255,255), 3)
                    #cv2.putText(dst, 'Square', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)


    cv2.imshow("Shapes", dst)
    key = cv2.waitKey(10)
    
    # plt.imshow(frame)
    plt.show()
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


