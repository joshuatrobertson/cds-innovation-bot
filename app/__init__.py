from flask import Flask

from db import init_db_engine
from .routes import main_routes
from slack import init_slack


def create_app(environment):
    app = Flask(__name__)

    # Load environment-specific configuration
    if environment == "development":
        app.config.from_object('config.DevelopmentConfig')
    elif environment == "testing":
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Register the Blueprints
    app.register_blueprint(main_routes)

    # Initialise the database engine and SQLAlchemy
    init_db_engine(app)

    return app
