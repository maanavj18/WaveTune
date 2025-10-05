import time
from gesture_utils import count_fingers

class FrameBuffer:
    def __init__(self, max_length = 10):
        self.max_length = max_length
        self.buffer = []

    def add_frame(self, hand_landmarks, handedness):
        finger_count = count_fingers(hand_landmarks, handedness)
        frame = {
            "finger_count": finger_count,
            "time" : time.time(),
            "handedness": handedness,
            "landmarks": hand_landmarks
        }
        self.buffer.append(frame)
        if len(self.buffer) > self.max_length:
            self.buffer.pop(0)
    
    def get_latest(self):
        if not self.buffer:
            return None
        else:
            return self.buffer[-1]
        
    def full_history(self):
        return self.buffer
        