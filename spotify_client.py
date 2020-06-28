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
        if response.ok:
            self.api_key = response.json()['access_token']
        else:
            message = "The refresh token is no longer valid."
            print(message)
            self.send_email(message)
            raise Exception

    def get_top_tracks_short(self):
        payload = {'limit': 30, 'time_range': 'short_term'}
        url = f'https://api.spotify.com/v1/me/top/tracks'
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            params=payload
        )
        if response.ok:
            tracks = response.json()['items']
            return tracks;
        else:
            message = "There was an error getting top tracks."
            print(message)
            self.send_email(message)
            raise Exception

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
            message = "There was an error creating a playlist."
            print(message)
            self.send_email(message)
            raise Exception


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
            message = "There was an error adding tracks to the playlist."
            print(message)
            self.send_email(message)
            raise Exception

    def get_recently_played(self, lastPlayed = 0):
        url = 'https://api.spotify.com/v1/me/player/recently-played'
        payload = {'limit': 50, 'after': lastPlayed}
        response = requests.get(
            url,
            params=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )
        if response.ok:
            track_objects = response.json()['items']
            return [(track['played_at'],track['track']['id']) for track in track_objects]
        else:
            message = "There was an error getting recently played tracks."
            print(message)
            self.send_email(message)
            raise Exception


    def get_tracks(self, track_ids):
        url = f'https://api.spotify.com/v1/tracks/'
        track_ids_string = ''
        first = True
        for track_id in track_ids:
            if first:
                track_ids_string += track_id
                first = False
            else:
                track_ids_string += ',' + track_id
        payload={'ids': track_ids_string}
        response = requests.get(
            url,
            params=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )
        if response.ok:
            tracks = response.json()['tracks']
            return {track['id']:(track['id'], track['name'], track['album']['name'], track['artists'][0]['name']) for track in tracks}
        else:
            message = "There was an error getting the tracks."
            print(message)
            self.send_email(message)
            raise Exception

    def send_email(self, message):
        import smtplib
        msg = f'Subject: SPOTIFY AUTOMATION ERROR \n\n{message}'
        fromaddr = 'uniqlohatchecker@gmail.com'
        toaddrs = ['andrewmniu@gmail.com']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("uniqlohatchecker@gmail.com", "5@Moz0h3f12KPXPqJ6")
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
