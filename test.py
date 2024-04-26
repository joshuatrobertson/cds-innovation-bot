from boxsdk import JWTAuth, Client, BoxAPIException

from app import config
from app.monday.functions import download_word_doc

# Initialize JWT Auth from the config file
jwt_auth = JWTAuth.from_settings_file('config.json')
client = Client(jwt_auth)

file_id='1513956073819'


"""Attempt to fetch a document and handle errors."""
try:
    file_item = client.file(file_id).get()
    print(f'Document Name: {file_item.name}')
    print('Successfully accessed the document!')
except BoxAPIException as e:
    if e.status == 403:
        print('Access Denied: Insufficient permissions.')
    elif e.status == 404:
        print('Document not found: Check the file ID.')
    else:
        print(f'API Error: {e.status} - {e.message}')
except Exception as e:
    print(f'An unexpected error occurred: {str(e)}')
