import os

from flask import Flask
from flask_migrate import Migrate

from api.v1.files import files
from db.pg_db import db, init_db


def create_app():
    app = Flask(__name__)

    environment = os.getenv('ENV')
    configuration = f'core.config.{environment}BaseConfig'

    app.config.from_object(configuration)
    app.register_blueprint(files, url_prefix='/api/v1/files')

    init_db(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.before_first_request
    def setup_db():
        db.create_all()

    @app.teardown_appcontext
    def close_db(sender, **extra):
        db.session.close()

    if not app.config['DEBUG']:
        import logging
        from logging.handlers import RotatingFileHandler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = RotatingFileHandler('logs/files_service.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    return app
