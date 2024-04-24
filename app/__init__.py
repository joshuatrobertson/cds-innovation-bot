from flask import Flask
from app.config import config
from app.routes import main_bp  # Ensure this matches the file where 'main_bp' is defined

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(main_bp)  # Register the blueprint
    return app