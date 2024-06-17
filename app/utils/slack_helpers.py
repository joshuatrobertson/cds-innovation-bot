import hashlib
import hmac
import json
import logging
import requests
from app.config import config

slack_closing_text = ("\n:nyan-josh: _This Slack App was built using Flask/ Python, "
                      "for any bugs or issues, please contact <@U06T3N4P2M8>_ :nyan-josh:")


def verify_slack_request(slack_signature, timestamp, data):
    try:
        slack_signing_secret = config.SLACK_SIGNING_SECRET.encode('utf-8')
        basestring = f'v0:{timestamp}:'.encode('utf-8') + data
        my_signature = 'v0=' + hmac.new(slack_signing_secret, basestring, hashlib.sha256).hexdigest()
        return hmac.compare_digest(my_signature, slack_signature)
    except Exception as e:
        logging.error("Error verifying Slack request", exc_info=True)
        return False


def open_modal(trigger_id, session_id, idea_text):
    # Serialise session_id and idea_text into a JSON string
    private_metadata = json.dumps({"session_id": session_id, "idea_text": idea_text})

    dialog = {
        "trigger_id": trigger_id,
        "view": {
            "type": "modal",
            "callback_id": "idea_modal",
            "private_metadata": private_metadata,
            "title": {"type": "plain_text", "text": "What is the impact?"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "block_idea_input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "idea_input",
                        "multiline": True
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "What is the expected impact of this idea? Who or what will it affect, and what is the significance of this?"
                    }
                }
            ]
        }
    }
    response = requests.post('https://slack.com/api/views.open', headers={
        "Authorization": f"Bearer {config.SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }, json=dialog)
    return response


def format_leaderboard_message(leaderboard_data, user_name):
    """Create a better-formatted leaderboard message to post to Slack."""
    # Define the emojis for the top three places
    emojis = [":first_place_medal:", ":second_place_medal:", ":third_place_medal:"]

    # Get the top three entries from the leaderboard data
    top_three = leaderboard_data[:3]

    # Find the user's position in the leaderboard
    user_position = next((idx for idx, entry in enumerate(leaderboard_data) if entry['_id'] == user_name), None)

    # Generate the user-specific message based on their position
    user_message = f"Your position on the leaderboard is: {user_position + 1}" if user_position is not None else \
        "You are not on the leaderboard. To get involved, submit your ideas using `/cdsidea` :smile:"

    # Start constructing the main message
    message_parts = [
        "Hello, and welcome to the *CDS Innovation Leaderboard* :trophy:",
        user_message,
        "For more information about CDS Innovation and how to get involved, please visit our w3 site (link TBC).",
        "*Leaderboard for this month:*"
    ]

    # Append formatted entries for the top three
    for idx, entry in enumerate(top_three):
        emoji = emojis[idx] if idx < len(emojis) else ":medal:"
        message_parts.append(f"{emoji} *{idx + 1}.* <@{entry['_id']}> - {entry['count']} ideas")

    # Add a closing text to encourage idea submission
    message_parts.append("_Let's keep the great ideas flowing! Submit your ideas using `/cdsidea`._")

    # Combine all parts into a single message string with newline separators
    message = "\n\n".join(message_parts) + "\n" + slack_closing_text

    return message

def post_to_slack(url, message):
    """ Post a message back to Slack using the response URL. """
    payload = {
        "text": message,
        "response_type": "ephemeral",
    }
    response = requests.post(url, json=payload)
    if not response.ok:
        print(f"Error posting to Slack: {response.text}")


def post_leaderboard_to_channel(leaderboard_data):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {config.SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚀 Monthly Innovation Idea Leaderboard 🚀"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here are the top contributors of innovative ideas this month:"
            }
        }
    ]

    for idx, entry in enumerate(leaderboard_data[:3]):
        emoji = [":first_place_medal:", ":second_place_medal:", ":third_place_medal:"][idx]
        user_tag = f"<@{entry['_id']}>"  # Assuming '_id' is the user's Slack ID
        blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"{emoji} *{idx + 1}.* {user_tag}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"{entry['count']} innovation ideas"
                }
            ]
        })

    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "Let's keep the great ideas flowing! Submit your ideas using `/submitidea`."
            }
        ]
    })

    blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": slack_closing_text
        }
    })

    data = {
        "channel": config.SLACK_CHANNEL_ID,
        "blocks": blocks,
        "text": "Monthly Innovation Leaderboard"  # This is for notification previews and older Slack clients
    }

    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        print(f"Failed to post message to Slack: {response.text}")
        return False
    return True

