import pytest
from flask import url_for, session
from app.core.auth import AuthManager

def test_index_page(client):
    """Test della homepage"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_about_page(client):
    """Test della pagina about"""
    response = client.get('/about')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'

def test_dashboard_page(client):
    """Test della dashboard (temporaneamente disattivata)"""
    response = client.get('/dashboard')
    assert response.status_code == 404

def test_404_page(client):
    """Test della pagina 404"""
    response = client.get('/pagina-non-esistente')
    assert response.status_code == 404

def test_template_rendering(client):
    """Test del rendering base dei template"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert '<!DOCTYPE html>' in response.data.decode()  # Verifica solo che sia HTML

def test_api_docs_route(client):
    """Test della route API docs"""
    response = client.get('/api/docs/')
    assert response.status_code == 200 