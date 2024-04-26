from flask import Blueprint

# Create a Blueprint
main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def index():
    return "Hello, World!"


@main_routes.route('/health')
def health():
    return 'OK', 200
