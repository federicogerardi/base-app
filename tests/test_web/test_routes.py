import pytest
from flask import url_for, session
from app.core.auth import AuthManager

def test_index_page(client):
    """Test della homepage"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Benvenuto' in response.data
    assert b'documentazione API' in response.data

def test_about_page(client):
    """Test della pagina about"""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_dashboard_page(client):
    """Test della dashboard (richiede autenticazione)"""
    # Test accesso senza autenticazione
    response = client.get('/dashboard')
    assert response.status_code == 401
    
    # Test accesso con autenticazione
    with client.application.app_context():
        # Crea un token di test
        token = AuthManager.create_token('test_user')
        headers = {'Authorization': f'Bearer {token}'}
        
        response = client.get('/dashboard', headers=headers)
        assert response.status_code == 200
        assert b'Dashboard' in response.data

def test_404_page(client):
    """Test della pagina 404"""
    response = client.get('/pagina-non-esistente')
    assert response.status_code == 404
    assert b'Not Found' in response.data

def test_template_rendering(client):
    """Test del rendering dei template"""
    response = client.get('/')
    html = response.data.decode()
    
    # 1. Verifica che sia HTML
    assert '<!DOCTYPE html>' in html
    assert '<html' in html
    
    # 2. Verifica contenuto essenziale
    assert 'Benvenuto' in html
    assert 'documentazione API' in html
    
    # 3. Verifica response
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_api_docs_link(client):
    """Test del link alla documentazione API"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'/api/docs/' in response.data 