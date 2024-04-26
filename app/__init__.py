from flask import Flask
from app.config import config
from app.routes import init_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    init_routes(app)
    return app
