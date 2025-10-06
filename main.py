# OpenCV and MediaPipe for hand tracking
import cv2
import mediapipe as mp

#Gesture Recognition and Frame Buffer
from frame_buffer import FrameBuffer
from configurable_gesture import ConfigurableGesture
from gesture_manager import GestureManager

# Spotify API Imports
import os
from dotenv import load_dotenv
from spotify_auth_manager import AuthManager
from spotify_client import SpotifyClient
from music_control import MusicController


def main():

    load_dotenv()

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")
    SCOPES = os.getenv("SCOPES")

    
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

    swipe_next_config = {
    'name': "swipe",
    'detection_type': 'movement',
    'target_value': None,
    'frame_threshold': None,
    'cooldown_frames': 30,
    'action': 'skip'
    }
    
    fist_gesture = ConfigurableGesture(fist_config)
    palm_gesture = ConfigurableGesture(palm_config)
    swipe_next_gesture = ConfigurableGesture(swipe_next_config)

    gesture_manager = GestureManager(controller)
    gesture_manager.register_gesture(fist_gesture)
    gesture_manager.register_gesture(palm_gesture)
    gesture_manager.register_gesture(swipe_next_gesture)


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
        print(frame_buffer.get_latest().get("landmarks").landmark[8].x)
                
        cv2.imshow("HandyMusic", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
