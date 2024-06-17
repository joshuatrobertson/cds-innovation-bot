import atexit
import pytz
from flask import Flask
from flask_session import Session
from app.config import config
from app.db.mongodb import get_ideas_leaderboard_for_month
from app.routes import init_routes
from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.slack_helpers import post_leaderboard_to_channel


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.secret_key = config.FLASK_SECRET_KEY
    app.config.from_object(config)
    init_routes(app)
    Session(app)
    return app


scheduler = BackgroundScheduler(timezone=pytz.timezone('Europe/London'))
scheduler.start()


def scheduled_leaderboard_post():
    leaderboard_data = get_ideas_leaderboard_for_month('ideas')
    post_leaderboard_to_channel(leaderboard_data)


# Scheduling the job
scheduler.add_job(scheduled_leaderboard_post, 'cron', hour='13')

# Ensure the scheduler is shut down properly when the app exits
atexit.register(lambda: scheduler.shutdown())
