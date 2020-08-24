from flask import Blueprint, current_app
from flask_socketio import SocketIO, join_room

from .config import Config
from .models import Message, db

bp = Blueprint('websocket', __name__)
socketio = SocketIO(async_mode='eventlet',
                    cors_allowed_origins=Config.CORS_ALLOWED_ORIGINS,
                    message_queue=Config.REDIS_URL)


@socketio.on('chat50.join')
def join_channel(message):
    join_room(message['channel'])
