def init_app(app):
    @app.route('/slack/commands', methods=['POST'])
    def handle_command():
        # Code to handle commands
        return 'Command received', 200
