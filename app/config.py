import os


class Config:
    FLASK_APP = 'app.py'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

    # Box API settings
    BOX_CLIENT_ID = os.environ.get('BOX_CLIENT_ID')
    BOX_CLIENT_SECRET = os.environ.get('BOX_CLIENT_SECRET')
    BOX_REDIRECT_URI = os.environ.get('BOX_REDIRECT_URI')
    BOX_JWT_CONFIG = os.environ.get('BOX_JWT_CONFIG', '/path/to/your/config.json')


# Instance of config to be used across the app
config = Config()
