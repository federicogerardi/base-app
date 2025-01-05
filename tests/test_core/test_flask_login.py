import pytest
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.core.database import db
from app.models.user import UserRole

@pytest.fixture
def test_user(app):
    """Fixture per creare un utente di test"""
    with app.app_context():
        user = User(
            email='test@example.com',
            username='test_user'
        )
        user.password = 'test_password'
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

def test_user_model_password(test_user):
    """Test della gestione password nel modello User"""
    # Test che la password sia hashata
    assert test_user._password != 'test_password'
    
    # Test verifica password
    assert test_user.check_password('test_password') is True
    assert test_user.check_password('wrong_password') is False

def test_user_login_logout(client):
    """Test login/logout"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    
    response = client.get('/auth/logout')
    assert response.status_code == 302  # redirect

def test_user_loader(app, test_user):
    """Test user loader"""
    with app.test_request_context():
        assert User.query.get(test_user.id) is not None

def test_user_to_dict(test_user):
    """Test conversione utente in dict"""
    user_dict = test_user.to_dict()
    assert user_dict['username'] == test_user.username
    assert user_dict['email'] == test_user.email
    assert 'password' not in user_dict

def test_user_role(test_user):
    """Test ruolo utente"""
    assert test_user.role in [UserRole.USER, UserRole.ADMIN]