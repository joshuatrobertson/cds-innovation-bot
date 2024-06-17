import logging
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    FLASK_APP = 'app.py'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')

    # Slack
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_SECRET = os.environ.get('SLACK_SECRET')
    SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    SLACK_CHANNEL_ID = 'C0710S8QY9Z'

    # Monday
    MONDAY_KEY = os.environ.get('MONDAY_KEY')
    MONDAY_BOARD_ID = os.environ.get('MONDAY_BOARD_ID')
    MONDAY_GROUP_ID = os.environ.get('MONDAY_GROUP_ID')

    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI')

    # Config

    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
    LOG_LEVEL = logging.INFO
    DEBUG = False
    TESTING = False

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = "/flask_session/"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True  # Mitigate XSS attacks


# Instance of config to be used across the app
config = Config()
