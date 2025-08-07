#day 1

#importing libraries
import cv2
import mediapipe as mp
import pygame
import numpy as np
import math
import time
import os


# learning the libraries/experimetning with them

# Displaying an image DEFAULT
'''
img = cv2.imread('porsche.jpg')
cv2.imshow('Image Window', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''

'''
cv2.rectangle(img, (50, 50), (200, 200), (255, 0, 0), 2)
cv2.circle(img, (150, 150), 50, (0, 255, 0), 3)
cv2.line(img, (0, 0), (300, 300), (0, 0, 255), 2)
cv2.putText(img, 'Hello World', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
'''


# Displaying webcam feed DEFAULT
capture = cv2.VideoCapture(0)

while True:
    success, frame = capture.read()
    if not success:
        break

    cv2.putText(frame, 'Hello World', (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (5, 5, 5), 2)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Webcam Feed', gray)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()



#loading + selecting music

#running file