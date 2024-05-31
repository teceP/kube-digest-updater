from .controllers.main_controller import main


def register_routes(app):
    app.register_blueprint(main)
