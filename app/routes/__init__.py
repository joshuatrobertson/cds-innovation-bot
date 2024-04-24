from flask import Blueprint
# Import blueprints from other route modules
from .slack_routes import slack_bp
from .box_routes import box_bp


def init_app(app):
    app.register_blueprint(slack_bp, url_prefix='/slack')
    app.register_blueprint(box_bp, url_prefix='/box')
