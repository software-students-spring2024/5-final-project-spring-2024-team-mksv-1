import pytest
import sys
from unittest.mock import patch
sys.path.append('../web_app')

from web_app import web_app as app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_game_title(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        response = client.post('/games/add', data={'title': 'test_game'})
        assert response.status_code == 302
        
def test_add_game_developer(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        response = client.post('/games/add', data={'developer': 'test_developer'})
        assert response.status_code == 302

def test_add_game_success(client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 201
        response = client.post('/games/add', data={'title': 'test_game', 'developer': 'test_developer'})
        assert response.status_code == 302


