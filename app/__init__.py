import logging
from flask import Flask
from flask_session import Session
from app.config import config
from app.db.mongodb import get_ideas_leaderboard_for_month
from app.routes import init_routes
from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.slack_helpers import post_leaderboard_to_channel
import atexit


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    Session(app)
    init_routes(app)

    @app.route('/')
    def home():
        return "Hello, World!"

    @app.route('/test_db')
    def test_db():
        try:
            results = get_ideas_leaderboard_for_month('ideas')
            return {"status": "success", "data": results}, 200
        except Exception as e:
            logging.error(f"Error during test_db: {e}")
            return {"status": "error", "message": str(e)}, 500

    return app


scheduler = BackgroundScheduler(timezone='Europe/London')
scheduler.start()


def scheduled_leaderboard_post():
    leaderboard_data = get_ideas_leaderboard_for_month('ideas')
    post_leaderboard_to_channel(leaderboard_data)


scheduler.add_job(scheduled_leaderboard_post, 'cron', minute='*/120')

atexit.register(lambda: scheduler.shutdown())