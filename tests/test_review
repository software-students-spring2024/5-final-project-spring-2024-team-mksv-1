from web_app.app import add_review 
from web_app.app import view_reviews 
import pytest
from unittest.mock import patch, MagicMock
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
