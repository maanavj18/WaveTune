

class Gesture:
    def __init__(self):
        pass

    def recognize(self, landmarks):
        """
        Input: landmarks from mediapipe
        Output: gesture name (string) or None
        """
        if not landmarks:
            return None

        # Example gesture: "THUMB_UP"
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        if thumb_tip.y < index_tip.y:  # y decreases upward in image coords
            return "THUMB_UP"

        return None