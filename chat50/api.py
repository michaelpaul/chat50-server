import json
from urllib.request import urlopen, Request
from flask import _request_ctx_stack
from flask import Blueprint, current_app, jsonify, request, g
from dateutil.parser import isoparse

from .auth import AuthError, requires_auth, get_token_auth_header
from .models import User, Message, db
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


@bp.route('/login', methods=['POST'])
@requires_auth
def login():
    # fetch profile from Auth0
    token = get_token_auth_header()
    url = 'https://' + current_app.config['AUTH0_DOMAIN'] + '/userinfo'
    req = Request(url, headers={
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    })
    res = urlopen(req)
    profile = json.loads(res.read())

    # create/update user
    user = User.query.filter_by(sub=profile['sub']).one_or_none()
    if user is None:
        user = User(sub=profile['sub'], nickname=profile['nickname'])

    user.email = profile['email']
    user.name = profile['name']
    user.picture = profile['picture']
    user.updated_at = isoparse(profile['updated_at'])

    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id})


@bp.route('/channels', methods=['GET'])
def get_channels():
    return jsonify([{'key': str(x), 'name': f'Week {x}'} for x in range(9)])


@bp.route('/messages/<channel>', methods=['GET'])
def get_messages(channel):
    messages = Message.query.filter_by(channel=channel).all()
    return jsonify([message.to_json() for message in messages])


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

    author = User.query.filter_by(sub=user['sub']).one()
    msg = Message(user=author, channel=channel, body=body)

    db.session.add(msg)
    db.session.commit()

    socketio.emit('chat50.message', msg.to_json())
    return jsonify({'id': msg.id})
