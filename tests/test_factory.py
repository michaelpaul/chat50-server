from chat50 import create_app
from chat50.websocket import socketio


def test_factory(monkeypatch):
    def init_app(app, **kwargs):
        return
    monkeypatch.setattr(socketio, 'init_app', init_app)

    assert create_app().env == 'production'
    assert create_app('testing').testing
    assert create_app('development').debug
    assert not create_app('production').debug


def test_app(app):
    assert app.testing
    assert app.config['REDIS_URL'] is None


def test_client(client):
    response = client.get('/')
    body = response.get_json()
    assert body['code'] == 404
    assert 'description' in body
