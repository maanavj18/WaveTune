class MusicController:
    def __init__(self, spotify_client):
        self.spotify = spotify_client

    def handle_gesture(self, gesture):
        if gesture == "play":
            self.spotify.play()
        elif gesture == "pause":
            self.spotify.pause()
        elif gesture == "skip":
            self.spotify.next_track()
        elif gesture == "back":
            self.spotify.previous_track()
        elif gesture.startswith("volume_"):
            level = int(gesture.split("_")[1])  # e.g., "volume_50"
            self.spotify.set_volume(level)
