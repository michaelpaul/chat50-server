import pytest

from chat50 import create_app
from chat50.models import db


@pytest.fixture
def app():
    app = create_app()

    # @TODO mock DB (SQLite)
    # with app.app_context():
    #     db.create_all()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
