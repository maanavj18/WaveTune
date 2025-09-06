import requests

class SpotifyClient:
    def __init__(self, auth_manager):
        self.auth = auth_manager

    def _headers(self):
        return {"Authorization": f"Bearer {self.auth.get_valid_token()}"}

    def play(self, device_id=None):
        url = "https://api.spotify.com/v1/me/player/play"
        params = {"device_id": device_id} if device_id else None
        requests.put(url, headers=self._headers(), params=params)

    def pause(self):
        url = "https://api.spotify.com/v1/me/player/pause"
        requests.put(url, headers=self._headers())

    def next_track(self):
        url = "https://api.spotify.com/v1/me/player/next"
        requests.post(url, headers=self._headers())

    def previous_track(self):
        url = "https://api.spotify.com/v1/me/player/previous"
        requests.post(url, headers=self._headers())

    def set_volume(self, volume_percent):
        url = "https://api.spotify.com/v1/me/player/volume"
        requests.put(url, headers=self._headers(), params={"volume_percent": volume_percent})
