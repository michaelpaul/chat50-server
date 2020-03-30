import os
from flask import Flask, render_template
from flask_cors import CORS

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('chat50.config.Config')
    
    # Init extensions
    from .models import db
    from .websocket import socketio
    db.init_app(app)
    socketio.init_app(app)
    CORS(app)

    # Blueprints
    app.register_blueprint(websocket.bp)

    # CLI
    app.cli.add_command(models.init_db_command)

    # Client
    @app.route('/')
    def index():
        return render_template('index.html')

    return app
