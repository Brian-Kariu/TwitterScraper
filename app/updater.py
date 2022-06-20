from apscheduler.schedulers.background import BackgroundScheduler
from app.serializers import trending_tweets


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(trending_tweets, 'interval', seconds=300)
    scheduler.start()
    print("Tweets have been updated")