import os
from flask import Flask
from flask_cors import CORS

from . import models, websocket, api


def create_app(config_name='production'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('chat50.config.' + config_name.capitalize())

    # Init extensions
    models.db.init_app(app)
    websocket.socketio.init_app(
        app,
        async_mode='eventlet',
        cors_allowed_origins=app.config['CORS_ALLOWED_ORIGINS'],
        message_queue=app.config['REDIS_URL']
    )
    CORS(app)

    # Blueprints
    app.register_blueprint(api.bp)

    # CLI
    app.cli.add_command(models.init_db_command)

    return app
