import os
import tempfile
import pytest
from server import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_get_none(client):
    """Start with a blank database."""

    rv = client.get('/get')
    assert len(json.loads(rv.data)) == 0
    assert rv.status_code == 200