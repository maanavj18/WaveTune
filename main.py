# main.py
import cv2
import mediapipe as mp

from frame_buffer import FrameBuffer
from configurable_gesture import ConfigurableGesture
from gesture_manager import GestureManager

from spotify_auth_manager import AuthManager
from spotify_client import SpotifyClient
from music_control import MusicController

CLIENT_ID = "ada7724248c14883881b4ed784027dc7"
CLIENT_SECRET = "7987ab4a8ff54158a664a22d9a9b9e3e"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPES = "user-read-playback-state user-modify-playback-state"

def main():

    auth = AuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    if not auth.access_token:  # first time
        auth.start_login(SCOPES)

    spotify = SpotifyClient(auth)
    controller = MusicController(spotify)
    frame_buffer = FrameBuffer(max_length=10)

    fist_config = {
    'name': 'pause_gesture',
    'detection_type': 'finger_count',
    'target_value': 0,
    'frame_threshold': 8,
    'cooldown_frames': 30,
    'action': 'pause'
    }
    palm_config = {
    'name': 'play_gesture',
    'detection_type': 'finger_count',
    'target_value': 5,
    'frame_threshold': 8,
    'cooldown_frames': 30,
    'action': 'play'
    }
    
    fist_gesture = ConfigurableGesture(fist_config)
    palm_gesture = ConfigurableGesture(palm_config)

    gesture_manager = GestureManager(controller)
    gesture_manager.register_gesture(fist_gesture)
    gesture_manager.register_gesture(palm_gesture)


    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

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
                #score = handedness.score   confidence
                frame_buffer.add_frame(hand_landmarks, label)

                # Draw landmarks (optional)
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style()
                )
        
        gesture_manager.update(frame_buffer)
                
        cv2.imshow("HandyMusic", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
