from datetime import datetime, date, timedelta
from spotify_client import SpotifyAPI
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval', minutes=5)
def main():
    today = date.today()
    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    lastMonth = lastMonth.strftime("%B %Y")

    api = SpotifyAPI()
    track_uris = [track['uri'] for track in api.get_top_tracks_short()]
    playlist_id = api.create_playlist(lastMonth)
    print(api.add_tracks_to_playlist(playlist_id, track_uris))

schedule.start()

if __name__ == '__main__':
    main()
