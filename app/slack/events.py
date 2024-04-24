def init_app(app):
    @app.route('/slack/events', methods=['POST'])
    def slack_events():
        # Handle the events from Slack here
        return 'OK', 200
