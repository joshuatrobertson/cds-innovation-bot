# Create a Blueprint for all Slack interactions
from flask import Blueprint

slack_bp = Blueprint('slack', __name__)

# Route for Slack events
@slack_bp.route('/events', methods=['POST'])
def slack_events():
    data = request.get_json()
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})

    if 'event' in data:
        event = data['event']
        if event['type'] == 'reaction_added' and event['item']['type'] == 'message':
            # Retrieve post ID from Slack timestamp
            post_id = retrieve_post_id_from_slack_ts(event['item']['ts'])
            if post_id:
                # Post exists, update database with reaction
                update_database_with_reaction(post_id, event)

    return jsonify(status="ok")


# Route for Slack commands
@slack_bp.route('/commands', methods=['POST'])
def slack_commands():
    user_id = request.form['user_id']
    command_text = request.form['text']
    channel_id = request.form['channel_id']
    command = request.form['command']
    if command == "/counter":
        post_id = create_post(command_text, channel_id, user_id)  # This function will create the post and track users
        return jsonify(response_type="in_channel", text=f"Message posted. Monitoring reactions for post id: {post_id}...")
    else:
        return jsonify(response_type="ephemeral", text=f"Received command '{command}', but I don't know what to do "
                                                       f"with it.")