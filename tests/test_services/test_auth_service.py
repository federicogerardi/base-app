import pytest
from app.services.auth_service import AuthService
from app.models import User
from flask_login import current_user

def test_register_user(app):
    """Test registrazione utente"""
    with app.app_context():
        success, message, user = AuthService.register_user(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        
        assert success is True
        assert user is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"

def test_login(app):
    """Test login utente"""
    with app.app_context():
        with app.test_request_context():
            # Prima registriamo un utente
            success, message, user = AuthService.register_user(
                email="test@example.com",
                username="testuser",
                password="password123"
            )
            assert success is True
            
            # Test login corretto
            success, message, user = AuthService.login(
                email="test@example.com",
                password="password123"
            )
            assert success is True
            assert user is not None
            assert current_user.is_authenticated

def test_logout(app):
    """Test logout utente"""
    with app.app_context():
        with app.test_request_context():
            # Prima registriamo e logghiamo un utente
            AuthService.register_user(
                email="test@example.com",
                username="testuser",
                password="password123"
            )
            AuthService.login(
                email="test@example.com",
                password="password123"
            )
            
            # Test logout
            success, message = AuthService.logout()
            assert success is True
            assert not current_user.is_authenticated 