# Spotify Automation
This project automates certain Spotify tasks with the Spotiy API, AP Scheduler, and a Heroku clock process.
### Monthly Playlists
One scheduled task is to get my top tracks over the last 4 weeks and add them to a playlist. This is run at the first of every month so that I can capture what I listen to every month.
### Listening History
The other scheduled task is to access my recently played tracks and store them in a database. The task is run every hour since the Spotify API only stores your 50 most recently played tracks.
