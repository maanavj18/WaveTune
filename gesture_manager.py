class GestureManager:
    def __init__(self, music_controller):
        self.music_controller = music_controller
        self.gestures = []

    def register_gesture(self, gesture):
        self.gestures.append(gesture)
    
    def update(self, frame_buffer):
        for gesture in self.gestures:
            result = gesture.update(frame_buffer)
            
            if result is not None:
                self._handle_gesture(result)
        
    def _handle_gesture(self, gesture):
        action = gesture["action"]
        self.music_controller.handle_gesture(action)


        
