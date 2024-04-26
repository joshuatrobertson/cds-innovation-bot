import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    FLASK_APP = 'app.py'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

    # Slack
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_SECRET = os.environ.get('SLACK_SECRET')
    SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')

    # Monday
    MONDAY_KEY = os.environ.get('MONDAY_KEY')
    MONDAY_BOARD_ID = os.environ.get('MONDAY_BOARD_ID')
    MONDAY_GROUP_ID = os.environ.get('MONDAY_GROUP_ID')


# Instance of config to be used across the app
config = Config()
