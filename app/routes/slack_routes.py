import datetime
import json

import requests
from flask import Blueprint, request, jsonify
import uuid
import time

from app import config
from app.db.mongodb import add_idea, get_ideas_leaderboard_for_month
from app.utils.slack_helpers import verify_slack_request, open_modal, format_leaderboard_message
from app.monday import MondayManager

slack_bp = Blueprint('slack', __name__)
monday_manager = MondayManager()


@slack_bp.route('/commands/idea', methods=['POST'])
def handle_idea():
    try:
        # Validate the timestamp and signature
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        if abs(time.time() - float(timestamp)) > 60 * 5:
            return "Request timeout", 403

        slack_signature = request.headers.get('X-Slack-Signature')
        if not verify_slack_request(slack_signature, timestamp, request.get_data()):
            return "Request verification failed!", 403

        # Extract necessary information
        trigger_id = request.form['trigger_id']
        user_name = request.form['user_name']
        idea_text = request.form['text']
        unique_session_id = str(uuid.uuid4())

        # Store data in MongoDB
        add_idea('ideas', {
            'trigger_id': trigger_id,
            'user_name': user_name,
            'idea_text': idea_text,
            'session_id': unique_session_id,
            'timestamp': time.time()
        })

        # Attempt to open the modal
        response = open_modal(trigger_id, unique_session_id, idea_text)
        if response.status_code == 200:
            return "", 200
        else:
            return jsonify({'response_type': 'ephemeral', 'text': 'Failed to open modal.'}), response.status_code
    except Exception as e:
        return jsonify({'response_type': 'ephemeral', 'text': str(e)}), 500


@slack_bp.route('/interactions', methods=['POST'])
def handle_explanation():
    try:
        payload = json.loads(request.form['payload'])
        user_name = payload['user']['name']
        # Fetch and deserialise the metadata passed through to the modal to keep state
        metadata = json.loads(payload['view']['private_metadata'])

        explanation = payload['view']['state']['values']['block_idea_input']['idea_input']['value']

        # Process the explanation data with Monday.com API
        column_values = {
            "text": metadata['idea_text'],
            "status": {"label": "New Idea"},
            "date4": {"date": datetime.datetime.now().strftime("%Y-%m-%d")},
            "name": user_name,
            "text__1": explanation
        }
        monday_manager.create_task(config.MONDAY_BOARD_ID, config.MONDAY_GROUP_ID, metadata['idea_text'],
                                   column_values)

        return "", 204
    except Exception as e:
        return jsonify({'response_type': 'ephemeral', 'text': str(e)}), 500


@slack_bp.route('/commands/leaderboard', methods=['POST'])
def leaderboard():
    try:
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        if abs(time.time() - float(timestamp)) > 60 * 5:
            return "Request timeout", 403

        slack_signature = request.headers.get('X-Slack-Signature')
        if not verify_slack_request(slack_signature, timestamp, request.get_data()):
            return "Request verification failed!", 403

        user_name = request.form['user_name']
        db_name = 'ideas'

        leaderboard_data = get_ideas_leaderboard_for_month(db_name)
        if not leaderboard_data:
            return jsonify({'response_type': 'ephemeral', 'text': 'Failed to retrieve leaderboard data'}), 500

        message = format_leaderboard_message(leaderboard_data, user_name)
        response_url = request.form['response_url']
        post_to_slack(response_url, message)

        return "", 200
    except Exception as e:
        return jsonify({'response_type': 'ephemeral', 'text': str(e)}), 500


def post_to_slack(url, message):
    """ Post a message back to Slack using the response URL """
    payload = {
        "text": message,
        "response_type": "ephemeral",
    }
    requests.post(url, json=payload)


def register_slack_routes(app):
    app.register_blueprint(slack_bp)
