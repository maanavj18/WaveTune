import json
import os 
import time
import requests
import base64
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer


class AuthManager:
    def __init__(self, client_id, client_secret, redirect_uri, token_file="tokens.json"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_file = token_file

        self.access_token = None
        self.refresh_token = None
        self.expires_at = None

        # Load tokens from file if it exists
        if os.path.exists(self.token_file):
            with open(self.token_file, "r") as f:
                tokens = json.load(f)
                self.access_token = tokens.get("access_token")
                self.refresh_token = tokens.get("refresh_token")
                self.expires_at = tokens.get("expires_at")
                print("🔑 Tokens loaded from file.")
        else:
            print("No saved tokens found — first-time login required.")

    def start_login(self, scopes):
        # Step 1: Build the Spotify authorization URL
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": scopes
        }
        auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
        print("👉 Go to this URL and log in:", auth_url)

        # Step 2: Spin up a local server to capture Spotify's redirect
        auth_code_holder = {}  # dict to hold auth_code across handler & main

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = urllib.parse.urlparse(self.path).query
                params = urllib.parse.parse_qs(query)

                if "code" in params:
                    auth_code_holder["code"] = params["code"][0]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Login successful! You can close this window.")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Missing authorization code.")

        # Run the server for a single request
        server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)
        print("📡 Waiting for Spotify login redirect...")
        server.handle_request()  # handles exactly one request

        # Step 3: Exchange code for tokens
        auth_code = auth_code_holder.get("code")
        token_resp = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        ).json()

        # Step 4: Save tokens + expiration
        self.access_token = token_resp["access_token"]
        self.refresh_token = token_resp["refresh_token"]
        self.expires_at = int(time.time()) + token_resp["expires_in"]

        with open(self.token_file, "w") as f:
            json.dump({
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_at": self.expires_at
            }, f)
        print("🔑 Tokens saved! You’re authenticated.")

    def refresh_access_token(self):

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            ).json()

   
        self.access_token = response["access_token"]
        self.expires_at = int(time.time()) + response["expires_in"]

        # Note: Spotify might not send a new refresh_token every time
        if "refresh_token" in response:
            self.refresh_token = response["refresh_token"]

        # Step 3: Save tokens to file again
        with open(self.token_file, "w") as f:
            json.dump({
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_at": self.expires_at
            }, f)

        print("♻️ Access token refreshed.")

    def get_valid_token(self):
        if not self.access_token or time.time() >= self.expires_at:
            print("⚠️ Token expired, refreshing...")
            self.refresh_access_token()
        return self.access_token




        

    
    

    
    

        
        
    
        
