from flask import Blueprint
from flask_socketio import SocketIO, join_room

socketio = SocketIO()


@socketio.on('chat50.join')
def join_channel(message):
    channel = message.get('channel')
    if channel:
        join_room(message['channel'])
