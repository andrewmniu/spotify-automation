from month_playlists import main as month_playlists
from listening_history import main as listening_history
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

scheduler.add_job(month_playlists, 'cron', day='1')
scheduler.add_job(listening_history, 'cron', hour='*')

scheduler.start()
