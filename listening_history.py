from spotify_client import SpotifyAPI
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import pytz

def main():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    # Connect to database
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
        print(message)
        print(e)
    mycursor = db.cursor()

    # Get most datetime of most recently added song
    mycursor.execute('SELECT MAX(played_at) FROM history')
    # Need to add 1 to timestamp since only neaerest second is stored, not microseconds
    lastPlayed = int((mycursor.fetchall()[0][0].timestamp() + 1) * 1000)
    print(lastPlayed)

    api = SpotifyAPI()
    history = api.get_recently_played(lastPlayed) # get history after last recorded song
    if(len(history) == 0):
        return

    # Gets track ids and gets full track objects from API
    track_ids = [track_object[1] for track_object in history]
    tracks_info = api.get_tracks(track_ids)

    # Convert to timezone aware datetimes and append Eastern time + rest of track info to entries list
    # Each entry is formatted as (played_at, track_id, name, album, artist)
    entries = []
    for i in range(0, len(history)):
        utcdate = datetime.strptime(history[i][0], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.UTC)
        entries.append((utcdate.astimezone(pytz.timezone('America/New_York')).strftime('%Y-%m-%d %H:%M:%S'),) + tracks_info[history[i][1]])

    # Insert tracks into database
    try:
        mycursor.executemany("INSERT IGNORE INTO tracks (id, name, album, artist) VALUES (%s, %s, %s, %s)", [track_object[1:] for track_object in entries])
        mycursor.executemany("INSERT INTO history (played_at, track_id) VALUES (%s, %s)", [track_object[:2] for track_object in entries])
        db.commit()
    except Exception as e:
        message = "There was an error inserting into database"
        api.send_email(message)
        print(message)
        print(e)
    else:
        print(entries)

if __name__ == "__main__":
    main()
