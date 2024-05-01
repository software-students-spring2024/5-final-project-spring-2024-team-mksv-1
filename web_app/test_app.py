import pytest
import sys
from unittest.mock import patch, MagicMock
sys.path.append('../web_app')
from flask import url_for

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


def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data  # Assuming the login form is displayed on the home page

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Login' in response.data  # Assuming the login form is displayed on the home page

def test_register(client):
    with patch('app.requests.post') as mock_post:
        # Mocking the API call
        mock_post.return_value.status_code = 201
        response = client.post('/register', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
        assert response.status_code == 200
        print(response.data)  # Print response data for debugging
        assert b'Registration successful! Please log in.' 

def test_invalid_registration_data(client):
    with patch('app.requests.post') as mock_post:
        # Mock the API call
        mock_post.return_value.status_code = 201  # Assuming registration is successful
        response = client.post('/register', data=dict(username='', password='testpassword'), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid username or password'


if __name__ == '__main__':
    pytest.main()

#test to see if user can post a review without being logged in (shouldn't be successful)
def test_add_review_not_logged_in(client):
    with client:
        #use mock session to simulate user not logged in
        with patch('flask.session', {}) as mock_session:
            response = client.post(url_for('add_review', game_id=1), data={'review': 'This game sucks!'}, follow_redirects=True)
            assert 'You must be logged in to add a review.' in response.get_data(as_text=True)

#test to see if user can post a review when they are logged in (should be successful)
def test_add_review_logged_in(client):
    with client:
        #again, use mock session and then requestss
        with patch('flask.session', {'user_id': 1}) as mock_session, \
             patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            response = client.post(url_for('add_review', game_id=1), data={'review': 'This game is mid'}, follow_redirects=True)
            assert 'Review added successfully!' in response.get_data(as_text=True)

def test_view_reviews(client):
    with client:
        #mock requests.get to simulate API response
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = [{'review': 'love it', 'user_id': 1}]
            response = client.get(url_for('view_reviews', game_id=1, game_title='Test Game'))
            assert 'love it' in response.get_data(as_text=True)
            assert 'Test Game' in response.get_data(as_text=True)
