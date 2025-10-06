import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set up webcam
cap = cv2.VideoCapture(0)

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # Flip for mirror view
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Print landmark positions
                landmarks = hand_landmarks.landmark
                for id, lm in enumerate(landmarks):
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 1)

        cv2.imshow("Hand Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()




"""
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

    
    frameConverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Webcam Feed', frameConverted)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()


#Mediapipe Hand Tracking
hands = mp.solutions.hands.Hands(
    staticimage_mode = False,
    max_num_hands = 2,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.5
)
def hand_tracking(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_Landmarks(
                frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)



"""
"""
if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
                """

"""# Example: convert a few key points to pixel coords
                wrist      = hand_landmarks.landmark[0]
                index_tip  = hand_landmarks.landmark[8]
                thumb_tip  = hand_landmarks.landmark[4]

                wx, wy = int(wrist.x * w), int(wrist.y * h)
                ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                tx, ty = int(thumb_tip.x * w), int(thumb_tip.y * h)

                # Show label and a simple pinch distance
                pinch_px = ((ix - tx)**2 + (iy - ty)**2) ** 0.5
                cv2.putText(frame, f"{label} ({score:.2f}) pinch:{int(pinch_px)}",
                            (wx, wy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
                # Count fingers
                finger_count = count_fingers(hand_landmarks, label)
                cv2.putText(frame, f"Fingers: {finger_count}", (wx, wy + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)"""