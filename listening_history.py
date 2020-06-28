from spotify_client import SpotifyAPI
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pytz
import pickle

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def main():
    with open("last_played.pickle", "rb") as pickle_file:
        lastPlayed = pickle.load(pickle_file)
    print(lastPlayed)

    api = SpotifyAPI()
    history = api.get_recently_played(lastPlayed)
    if(len(history) == 0):
        return
    track_ids = [track_object[1] for track_object in history]
    tracks_info = api.get_tracks(track_ids)

    entries = []
    for i in range(0, len(history)):
        utcdate = datetime.strptime(history[i][0], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)
        if i == 0:
            with open("last_played.pickle", "wb") as pickle_file:
                pickle.dump(int(utcdate.timestamp()*1000), pickle_file)
            print(int(utcdate.timestamp()*1000))
        entries.append((utcdate.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S'),) + tracks_info[history[i][1]])

    try:
        db = mysql.connector.connect(
            host="bnxju3rtfsxvdnrkpfha-mysql.services.clever-cloud.com",
            user="ugogfxi4hlfl0paq",
            password=os.getenv('DB_PASSWORD'),
            database="bnxju3rtfsxvdnrkpfha"
        )
    except Exception as e:
        message = "There was an error connecting to the database."
        api.send_email(message)
        print(e)
    else:
        mycursor = db.cursor()
        mycursor.executemany("INSERT IGNORE INTO tracks (id, name, album, artist) VALUES (%s, %s, %s, %s)", [track_object[1:] for track_object in entries])
        mycursor.executemany("INSERT INTO history (played_at, track_id) VALUES (%s, %s)", [track_object[:2] for track_object in entries])
        db.commit()
        print(entries)


if __name__ == "__main__":
    main()