import pytest
from app.models import User
from app.core.database import db

@pytest.fixture
def test_user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }

def test_login_page(client):
    """Test della pagina di login"""
    response = client.get('/auth/login')
    assert response.status_code == 200

def test_register_page(client):
    """Test della pagina di registrazione"""
    response = client.get('/auth/register')
    assert response.status_code == 200

def test_registration_process(client, test_user_data):
    """Test del processo di registrazione"""
    response = client.post('/auth/register', data={
        **test_user_data,
        'confirm_password': test_user_data['password']
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_process(client, test_user_data):
    """Test del processo di login"""
    # Prima registriamo un utente
    client.post('/auth/register', data={
        **test_user_data,
        'confirm_password': test_user_data['password']
    })
    
    # Test login
    response = client.post('/auth/login', data={
        'email': test_user_data['email'],
        'password': test_user_data['password']
    }, follow_redirects=True)
    assert response.status_code == 200

def test_logout_process(client, test_user_data):
    """Test del processo di logout"""
    # Prima registriamo e logghiamo un utente
    client.post('/auth/register', data={
        **test_user_data,
        'confirm_password': test_user_data['password']
    })
    client.post('/auth/login', data={
        'email': test_user_data['email'],
        'password': test_user_data['password']
    })
    
    # Test logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200 