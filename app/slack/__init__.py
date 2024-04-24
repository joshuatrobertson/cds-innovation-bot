def init_app(app):
    from . import events, commands
    commands.init_app(app)
    events.init_app(app)
