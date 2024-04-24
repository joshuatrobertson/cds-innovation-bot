from flask import Flask
from .routes import slack_bp


def init_slack(app):
    # Register the Blueprint with the Flask app
    app.register_blueprint(slack_bp, url_prefix='/slack')
