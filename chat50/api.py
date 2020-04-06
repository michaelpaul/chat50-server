from flask import _request_ctx_stack
from flask import Blueprint, current_app, jsonify, request, g

from .auth import AuthError, requires_auth
from .models import Message, db
from .websocket import socketio

bp = Blueprint('api', __name__, url_prefix='/api')


def current_user():
    ctx = _request_ctx_stack.top
    if ctx is not None:
        return ctx.current_user


class ApiError(Exception):
    def __init__(self, description, status_code=None):
        Exception.__init__(self)
        self.description = description
        self.status_code = status_code or 400


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@bp.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify({
        'code': error.status_code,
        'description': error.description
    })
    response.status_code = error.status_code
    return response


@bp.route('/channels', methods=['GET'])
def get_channels():
    return jsonify([{'key': str(x), 'name': f'Week {x}'} for x in range(9)])


@bp.route('/messages/<channel>', methods=['GET'])
def get_messages(channel):
    messages = Message.query.filter_by(channel=channel).all()
    return jsonify([
        {
            'author': "Cloud",
            'avatar': "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
            'body': message.body,
            'datetime': message.created_at
        } for message in messages
    ])


@bp.route('/messages', methods=['POST'])
@requires_auth
def post_message():
    params = request.get_json()
    body = params.get('message')
    channel = params.get('channel')
    user = current_user()

    if not user:
        raise ApiError('Empty user')
    if not channel:
        raise ApiError('Empty channel')
    if not body:
        raise ApiError('Empty message')

    msg = Message(author_id=user['sub'], channel=channel, body=body)
    db.session.add(msg)
    db.session.commit()

    response = {'id': msg.id}
    socketio.emit('chat50.message', response)
    return jsonify(response)
