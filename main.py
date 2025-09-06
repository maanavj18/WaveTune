# main.py
import cv2
import mediapipe as mp
from gesture.tracking import HandTracker
from gesture.gesture_comp import Gesture

from spotify_auth_manager import AuthManager
from spotify_client import SpotifyClient
from music_control import MusicController

CLIENT_ID = "ada7724248c14883881b4ed784027dc7"
CLIENT_SECRET = "7987ab4a8ff54158a664a22d9a9b9e3e"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-read-playback-state user-modify-playback-state"

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


def main():

    auth = AuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if not auth.access_token:  # first time
        auth.start_login(SCOPES)

    # 2. Spotify client
    spotify = SpotifyClient(auth)

    # 3. Music controller
    controller = MusicController(spotify)

    # 4. Example: simulate gesture inputs
    #controller.handle_gesture("play")
    #controller.handle_gesture("volume_50")
    

    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    recognizer = Gesture()
    #controller = MusicController()
    
    mp_hands =mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(frame_RGB)

        h, w = frame.shape[:2]

        if results.multi_hand_landmarks:
            # Pair each hand's landmarks with its handedness by index.
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[i].classification[0]
                label = handedness.label  # "Left" or "Right"
                score = handedness.score  # confidence

                # Draw landmarks (optional)
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style()
                )

                # Example: convert a few key points to pixel coords
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
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)
                
                
                if finger_count == 5:
                    count+=1
                    if(count == 5):
                        controller.handle_gesture("play")
                        controller.handle_gesture("volume_50")
                else:
                    count = 0
                

        cv2.imshow("HandyMusic", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
