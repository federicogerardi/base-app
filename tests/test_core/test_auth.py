import pytest
from flask import jsonify
from datetime import timedelta
from app.core.auth import AuthManager, auth_required
from flask_jwt_extended import create_access_token

def test_token_creation(app):
    """Test della creazione del token"""
    with app.app_context():
        # Test creazione token base
        token = AuthManager.create_token('test_user')
        assert token is not None
        
        # Test creazione token con scadenza personalizzata
        token = AuthManager.create_token('test_user', timedelta(hours=1))
        assert token is not None

def test_protected_route(app, client):
    """Test delle route protette"""
    @app.route('/test-auth')
    @auth_required
    def protected():
        return jsonify({'success': True, 'message': 'Accesso consentito'})

    # Test accesso senza token
    response = client.get('/test-auth')
    assert response.status_code == 401
    assert not response.json['success']
    
    # Test accesso con token valido
    with app.app_context():
        token = AuthManager.create_token('test_user')
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/test-auth', headers=headers)
        assert response.status_code == 200
        assert response.json['success']

def test_expired_token(app, client):
    """Test del comportamento con token scaduto"""
    @app.route('/test-expired')
    @auth_required
    def protected():
        return jsonify({'success': True})

    with app.app_context():
        # Crea un token già scaduto
        token = create_access_token('test_user', expires_delta=timedelta(seconds=-1))
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/test-expired', headers=headers)
        assert response.status_code == 401
        assert not response.json['success']
        assert 'scaduto' in response.json['message'].lower()

def test_invalid_token(app, client):
    """Test del comportamento con token non valido"""
    @app.route('/test-invalid')
    @auth_required
    def protected():
        return jsonify({'success': True})

    # Test con token malformato
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get('/test-invalid', headers=headers)
    assert response.status_code == 401
    assert not response.json['success']
    assert 'non valido' in response.json['message'].lower() 