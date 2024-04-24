def init_app(app):
    from . import box_integration
    box_integration.init_app(app)