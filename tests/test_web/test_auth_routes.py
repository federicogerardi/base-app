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

def test_logout_route(client):
    """Test della route di logout"""
    response = client.get('/auth/logout')
    # Redirect perché non autenticato
    assert response.status_code == 302 