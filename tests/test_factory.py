from chat50 import create_app


def test_factory():
    assert not create_app().testing
    # @TODO
    # assert create_app({'TESTING': True}).testing


def test_client(client):
    response = client.get('/')
    body = response.get_json()
    assert body['code'] == 404
    assert 'description' in body
