import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    # Test successful registration
    response = client.post('/register', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful! Please log in.' in response.data

    # Test registration with existing username
    response = client.post('/register', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Username already exists' in response.data

def test_login(client):
    # Test successful login
    response = client.post('/login', data=dict(username='testuser', password='testpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Login successful!' in response.data

    # Test login with invalid credentials
    response = client.post('/login', data=dict(username='invaliduser', password='invalidpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data
