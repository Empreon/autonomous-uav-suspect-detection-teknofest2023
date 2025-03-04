import cv2
import numpy as np

def colorProcess(frame):
    data_set = []
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300: #100
            x, y, w, h = cv2.boundingRect(cnt)
            data_set.append([x, y, w, h])
            
    return data_set
