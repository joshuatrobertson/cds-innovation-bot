# Import blueprints from other route modules
from .slack_routes import slack_bp
from .main_routes import main_routes


def init_routes(app):
    app.register_blueprint(slack_bp, url_prefix='/slack')
    app.register_blueprint(main_routes)
