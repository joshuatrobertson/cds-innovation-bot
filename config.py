import datetime
from boxsdk import JWTAuth, Client
from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()


class Config:
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
    DEBUG = False
    TESTING = False
    auth = JWTAuth(
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_SECRET'),
        enterprise_id=os.getenv('ENTERPRISE_ID'),
        jwt_key_id=os.getenv('JWT_KEY_ID'),
        rsa_private_key_file_sys_path='path/to/your_private_key.pem',
        rsa_private_key_passphrase=os.getenv('CLIENT_ID').encode()
    )
    LOG_LEVEL = logging.INFO


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = logging.INFO

    DEBUG = True


class ProductionConfig(Config):
    LOG_LEVEL = logging.WARNING

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Set log file name with date
    LOG_FILE = f'logs/logs_response_counter{current_date}.log'

    # Configure logging to output to file
    LOGGING_CONFIG = {
        'version': 1,
        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'filename': LOG_FILE,
                'level': LOG_LEVEL,
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file_handler'],
                'level': LOG_LEVEL,
                'propagate': False,
            },
        },
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
    }
