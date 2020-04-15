from flask import Blueprint, current_app
from flask_socketio import SocketIO, emit, send

from .models import Message, db

bp = Blueprint('websocket', __name__)
socketio = SocketIO(async_mode='eventlet', cors_allowed_origins=['http://localhost:3000'])


@socketio.on('chat message')
def test_message(message):
    msg = Message(body=message)
    db.session.add(msg)
    db.session.commit()
    current_app.logger.info('message saved')

    # mandar mensagem para o remetente
    emit('pra vc', 'recebi sua mensagem')
    # mandar pra geral
    emit('chat message', message, broadcast=True)


@socketio.on('connect')
def client_connected():
    current_app.logger.info('new client connected')


@socketio.on('disconnect')
def client_disconnected():
    current_app.logger.info('client has gonne away')
