# main.py
import cv2
from gesture.tracking import HandTracker
from gesture.gesture_comp import Gesture
from music_control.player import MusicController

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = GestureRecognizer()
    controller = MusicController("assets/sapne-bande.mp3")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = tracker.process_frame(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                gesture = recognizer.recognize(landmarks)
                if gesture:
                    controller.handle_gesture(gesture)

        cv2.imshow("HandyMusic", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
