import numpy as np




def count_fingers(hand_landmarks, handedness):
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []
        # Thumb
    if handedness == "Right":
        if hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:  # Left hand
        if hand_landmarks.landmark[finger_tips_ids[0]].x > hand_landmarks.landmark[finger_tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other four fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[finger_tips_ids[id]].y < hand_landmarks.landmark[finger_tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)
    
    

    