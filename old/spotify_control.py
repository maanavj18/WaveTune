import requests
ACCESS_TOKEN = "BQA3HzObxRuSqEy8-CE50k3KLp9uvdjOYbmt4dq735vPSRmPLa9UAycp8GwQbPDtZcMgfrEtqZVtzwJ32MKsw7Tt_3-RIah39D0NQ6hZ6GhsYCyH6BFOecs-iK38iOXjwidgxxE9GzGdGJIC5ovPc-zzkJApS4nhXkPTxSB8oQ8iV2_kCkBW87QgWk18gIoIJUM7FWevY1bHUEFIdBgst4jAVolH3xtsH07BkkiL7OWj0c1P6iKgBQ0".replace(" ", "").replace("\n", "")
refresh_token = "AQD9F7AegjilPNvgZVBRJb3oYY8iJA80KjITs9T9ky-Ve-Ko4UrnyvsR-gYEM6kgd69AnTxCHNo60gqerHHi-hIAwdBOmN9P5tCL23nMbC0j-eK6UHIVflIVDNm6MYxDEPU".replace(" ", "").replace("\n", "")

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 1️⃣ Play / Resume
def play():
    url = "https://api.spotify.com/v1/me/player/play"
    response = requests.put(url, headers=HEADERS)
    print(response.status_code, response.text)

# 2️⃣ Pause
def pause():
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers=HEADERS)
    print(response.status_code, response.text)

# 3️⃣ Skip to Next Track
def next_track():
    url = "https://api.spotify.com/v1/me/player/next"
    response = requests.post(url, headers=HEADERS)
    print(response.status_code, response.text)

# 4️⃣ Skip to Previous Track
def previous_track():
    url = "https://api.spotify.com/v1/me/player/previous"
    response = requests.post(url, headers=HEADERS)
    print(response.status_code, response.text)

# 5️⃣ Set Volume (0–100)
def set_volume(volume_percent):
    url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume_percent}"
    response = requests.put(url, headers=HEADERS)
    print(response.status_code, response.text)

# Example usage:
#play()
#pause()
next_track()
# previous_track()
# set_volume(50)
