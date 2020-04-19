from flask import Blueprint, current_app
from flask_socketio import SocketIO, join_room

from .models import Message, db

bp = Blueprint('websocket', __name__)
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins=[
    'http://localhost:3000',
    'https://3000-d0bf3d31-292f-4ca8-b2af-6abd5e2548b0.ws-eu01.gitpod.io'
])


@socketio.on('chat50.join')
def join_channel(message):
    join_room(message['channel'])