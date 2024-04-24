from flask import Blueprint, jsonify
from boxsdk import OAuth2, Client

box_bp = Blueprint('box', __name__)


@box_bp.route('/folders')
def list_folders():
    # Example: set up OAuth2 and client; securely handle setup
    client = Client(OAuth2(
        client_id='your-client-id',
        client_secret='your-client-secret',
        access_token='your-access-token',
    ))
    root_folder = client.folder(folder_id='0').get()
    items = root_folder.get_items(limit=100)
    return jsonify([item.name for item in items])
