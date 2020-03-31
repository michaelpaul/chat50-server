from flask import Blueprint, current_app, jsonify, request

bp = Blueprint('api', __name__, url_prefix='/api')

# public
@bp.route('/messages', methods=['GET'])
def get_messages():
    return jsonify([
        {'body': 'foo'}, 
        {'body': 'bar'}
    ])

# protected
@bp.route('/messages', methods=['POST'])
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
