import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands = max_num_hands,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
            )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def processFrame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        hands_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
                )
                hands_landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

        return frame, hands_landmarks
    
    def close(self):
        self.hands.close()
            
        
    