import sys
import os
import re

# Change the current working directory to the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    html_content = response.data.decode('utf-8')
    regex_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    assert "IP" in html_content
    assert re.search(regex_pattern, html_content), "No IP address found in response"

def test_json_response(client):
    response = client.get('/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'ip' in json_data
    regex_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    assert re.search(regex_pattern, json_data['ip']), "No valid IP address found in JSON response"

def test_invalid_route(client):
    response = client.get('/invalid')
    assert response.status_code == 404
    assert b'Not Found' in response.data