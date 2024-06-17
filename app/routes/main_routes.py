from flask import Blueprint
from flask import session

# Create a Blueprint
main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/')
def index():
    return "Hello, World!"


@main_routes.route('/set/<string:value>')
def set_session(value):
    session["key"] = value
    return "<h1>Ok</h1>"


@main_routes.route('/get')
def get_session():
    session_contents = [(key, session[key]) for key in session]
    return f"Session contents: {session_contents}"


@main_routes.route('/health')
def health():
    return 'OK', 200
