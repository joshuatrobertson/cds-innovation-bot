from flask import request, jsonify, current_app
from boxsdk import OAuth2, Client
import os


def init_app(app):
    oauth = OAuth2(
        client_id=os.getenv('BOX_CLIENT_ID'),
        client_secret=os.getenv('BOX_CLIENT_SECRET')
    )
    client = Client(oauth)

    app.route('/box/update/<file_id>', methods=['POST'])

    def update_file(file_id):
        """
        Updates the content of an existing file.
        """
        try:
            file_to_update = client.file(file_id=file_id)
            content = request.files['file']

            # Upload a new version of the file
            updated_file = file_to_update.update_contents_with_stream(content.stream)

            return jsonify({'file_id': updated_file.id, 'file_name': updated_file.name,
                            'message': 'File updated successfully.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/box/auth')
    def box_auth():
        auth_url, csrf_token = oauth.get_authorization_url('https://your-redirect-uri.com')
        return jsonify({'auth_url': auth_url})

    @app.route('/box/callback')
    def box_callback():
        code = request.args.get('code')
        access_token, refresh_token = oauth.authenticate(code)
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

    @app.route('/box/upload', methods=['POST'])
    def upload_file():
        file = request.files['file']
        folder_id = '0'  # Root folder is '0'
        new_file = client.folder(folder_id).upload_stream(file.stream, file.filename)
        return jsonify({'file_id': new_file.id, 'file_name': new_file.name})

    @app.route('/box/download/<file_id>', methods=['GET'])
    def download_file(file_id):
        file_contents = client.file(file_id).content()
        return file_contents
