import pytest
import sys
from unittest.mock import patch

sys.path.append("../web_app")

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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
