from importlib import import_module
from os import environ
from flask import Flask
from project.extensions import mail, celery, csrf, db
from project.blueprints import all_blueprints


def create_app():

    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(
        environ.get('APP_SETTINGS', 'config.DevelopmentConfig')
    )
    with app.app_context():
        for module in app.config.get('DB_MODELS_IMPORT', list()):
            import_module(module)

    for bp in all_blueprints:
        import_module(bp.import_name)
        app.register_blueprint(bp)

    db.init_app(app)
    mail.init_app(app)
    celery.init_app(app)
    csrf.init_app(app)

    return app