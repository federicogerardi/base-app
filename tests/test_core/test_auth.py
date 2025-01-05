import pytest
from datetime import timedelta
from flask import jsonify
from flask_login import current_user, login_user, logout_user
from app.core.auth import auth_required, AuthManager
from flask_jwt_extended import create_access_token

def test_token_creation(app):
    """Test della creazione del token"""
    with app.test_request_context():
        # Verifica che le chiavi siano impostate
        assert app.config['JWT_SECRET_KEY'] is not None
        assert app.config['SECRET_KEY'] is not None
        
        token = AuthManager.create_token('test_user')
        assert token is not None
        assert isinstance(token, str)

def test_protected_route(app, client):
    """Test delle route protette"""
    @app.route('/test-auth')
    @auth_required
    def protected():
        return jsonify({'success': True, 'message': 'Accesso consentito'})

    with app.test_request_context():
        # Test accesso senza token
        response = client.get('/test-auth')
        assert response.status_code == 401
        assert not response.json['success']

        # Test accesso con token valido
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

    with app.test_request_context():
        # Crea un token già scaduto
        token = create_access_token(
            'test_user',
            expires_delta=timedelta(seconds=-1)
        )
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get('/test-expired', headers=headers)
        assert response.status_code == 401

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