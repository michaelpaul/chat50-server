import pytest

from chat50 import create_app
from chat50.models import db
from chat50.websocket import socketio


@pytest.fixture
def app():
    app = create_app('testing')
    # @TODO mock DB (SQLite)
    # with app.app_context():
    #     db.create_all()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def socket(app):
    return socketio.test_client(app)
