
class ConfigurableGesture:

    IDLE = "idle"
    DETECTING = "detecting"
    CONFIRMED = "confirmed"
    COOLDOWN = "cooldown"

    def __init__(self, config):
        self.name = config["name"]
        self.detection_type = config["detection_type"]
        self.target_value = config["target_value"]
        self.frame_threshold = config["frame_threshold"]
        self.cooldown_frames = config["cooldown_frames"]
        self.action = config["action"]
        
        self.state = self.IDLE
        self.frame_count = 0
        self.cooldown_count = 0

    def _check_detection(self, frame_data):
        if self.detection_type == "finger_count":
            return self.target_value == frame_data["finger_count"]
        
        return False
    
    def update(self, frame_buffer):
        last_frame = frame_buffer.get_latest()
        if not last_frame:
            return None
        
        if self.state == self.COOLDOWN:
            self.cooldown_count += 1
            if self.cooldown_count >= self.cooldown_frames:
                self.state = self.IDLE
                self.cooldown_count = 0
                return None
        
        if self._check_detection(last_frame):
            

        
        

        
        
