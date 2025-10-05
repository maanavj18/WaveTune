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
class GestureUtils:
    def __init__(self):
        pass # Placeholder for future initialization
    
    def calculate_distance(point1, point2):
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)
    
    def angle_between(p1, p2, p3, p4):
        v1 = np.array([p2.x - p1.x, p2.y - p1.y, p2.z - p1.z])
        v2 = np.array([p4.x - p3.x, p4.y - p3.y, p4.z - p3.z])
        angle = np.arccos(np.clip(np.dot(v1, v2)) / (np.linalg.norm(v1) *np.linalg.norm(v2)))
        return np.degrees(angle)
    
    def hand_displacement(hand_history, current_hand):
        pass  # Placeholder for future implementation

    