from flask import Blueprint, current_app, jsonify, request

from .auth import AuthError, requires_auth

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@bp.route('/channels', methods=['GET'])
def get_channels():
    return jsonify([{'key': str(x), 'name': f'Week {x}'} for x in range(9)])

# public
@bp.route('/messages', methods=['GET'])
def get_messages():
    return jsonify([
        {
            'author': "Cloud",
            'avatar': "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
            'body': 'foo',
            'datetime': 'yesterday'
        },
        {
            'author': "Squall",
            'avatar': "https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png",
            'body': 'bar',
            'datetime': 'today'
        },
    ])

# protected
@bp.route('/messages', methods=['POST'])
@requires_auth
def post_message():
    # persist msg
    # publish on the realtime channel
    # socketio.emit('chat-message', {'content': 'request.get("content")'})
    params = request.get_json()

    return jsonify({
        'id': 'generated id',
        'author': 'logged in user',
        'message': params['message']
    })
