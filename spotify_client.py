import requests
import base64
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class SpotifyAPI(object):
    def __init__(self):
        CLIENT_ID = os.getenv('CLIENT_ID')
        CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')
        # redirect_uri = 'http://localhost:8888/callback'

        # scope = 'user-top-read%20playlist-modify-public'

        encoded = base64.standard_b64encode(bytes(f"{CLIENT_ID}:{CLIENT_SECRET}", 'utf-8'))
        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(
            url,
            headers={
                'Content-type':'application/x-www-form-urlencoded',
                "Authorization": f"Basic {encoded.decode()}"
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": REFRESH_TOKEN
            }
        )
        self.api_key = response.json()['access_token']
        print(self.api_key)


    def get_top_tracks_short(self):
        limit = 30
        time_range = 'short_term'
        url = f'https://api.spotify.com/v1/me/top/tracks?limit={limit}&time_range={time_range}'
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )
        tracks = response.json()['items']
        return tracks;

    def create_playlist(self, month):
        url = 'https://api.spotify.com/v1/users/andrewniu/playlists'
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "name": month,
                "description": f"My top tracks of {month}"
            }
        )
        if(response.ok):
            return response.json()['id']
        else:
            return "Error"

    def add_tracks_to_playlist(self, playlist_id, track_uris):
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json={
                "uris": track_uris,
            }
        )
        if(response.ok):
            return "Playlist Created!"
        else:
            return "Error"
