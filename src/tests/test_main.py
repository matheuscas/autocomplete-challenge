import json
from main import app as my_app
import pytest


@pytest.yield_fixture
def app():
    yield my_app

@pytest.fixture
def test_cli(loop, app, test_client):
    return loop.run_until_complete(test_client(app))

async def test_fails_event_not_present(test_cli):
    payload = {
        'timestamp': '2016-09-22T13:57:31.2311892-04:00'
    }
    response = await test_cli.post('/navigation/info', data=json.dumps(payload))
    assert response.status == 404

async def test_fails_timestamp_not_present(test_cli):
    payload = {
        'event': 'buy'
    }
    response = await test_cli.post('/navigation/info', data=json.dumps(payload))
    assert response.status == 404

async def test_success_200(test_cli):
    payload = {
        "event":"buy", 
        "timestamp":"2016-09-22T13:57:31.2311892-04:00"
    }
    response = await test_cli.post('/navigation/info', data=json.dumps(payload))
    assert response.status == 200
