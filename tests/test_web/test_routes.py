import pytest
from flask import url_for, session
from app.core.auth import AuthManager

def test_index_page(client):
    """Test della homepage"""
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_page(client):
    """Test della pagina dashboard"""
    response = client.get('/dashboard')
    # Redirect al login perché non autenticato
    assert response.status_code == 302

def test_users_page(client):
    """Test della pagina dashboard"""
    response = client.get('/dashboard/users')
    # Redirect al login perché non autenticato
    assert response.status_code == 302

def test_404_page(client):
    """Test della pagina 404"""
    response = client.get('/pagina-non-esistente')
    assert response.status_code == 404