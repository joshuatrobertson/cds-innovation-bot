import datetime
import hashlib
import hmac
import os
import time

from flask import Blueprint, request, jsonify

from app import config
from app.monday import MondayManager

monday_manager = MondayManager()

slack_bp = Blueprint('slack', __name__)


@slack_bp.route('/commands/idea', methods=['POST'])
def handle_idea():
    try:
        timestamp = request.headers.get('X-Slack-Request-Timestamp')
        if abs(time.time() - float(timestamp)) > 60 * 5:
            return "Request timeout", 403

        slack_signature = request.headers.get('X-Slack-Signature')
        if not verify_slack_request(slack_signature, timestamp, request.get_data()):
            return "Request verification failed!", 403
    except ValueError as e:
        return str(e), 500

    user_name = request.form['user_name']
    idea_text = request.form['text']
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    column_values = {
        "text": idea_text,
        "status": {"label": "New Idea"},
        "date": {"date": date},
        "creator": {"text": user_name}
    }

    result = monday_manager.create_task(config.MONDAY_BOARD_ID, config.MONDAY_GROUP_ID, idea_text, column_values)

    if result and result.get('data'):
        return jsonify({
            "response_type": "ephemeral",
            "text": f"Thanks, <@{user_name}>. Your idea ({idea_text}) has been recorded!"
        })
    else:
        error_message = result.get('errors', [{'message': 'Unknown error'}])[0][
            'message'] if result else 'No response from API'
        return jsonify({
            "response_type": "ephemeral",
            "text": f"Failed to add idea by <@{user_name}>. Please try again. Error: {error_message}"
        })


def verify_slack_request(slack_signature, timestamp, data):
    slack_signing_secret = config.SLACK_SIGNING_SECRET
    # Ensure the signing secret is bytes
    slack_signing_secret = slack_signing_secret.encode('utf-8')

    # Construct the basestring as Slack expects
    basestring = f'v0:{timestamp}:'.encode('utf-8') + data  # data should be bytes

    # Use hmac to compute signature
    my_signature = 'v0=' + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()

    # Compare the computed signature to the one provided by Slack
    return hmac.compare_digest(my_signature, slack_signature)
