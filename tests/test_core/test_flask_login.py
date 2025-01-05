import pytest
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.core.database import db

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
    assert test_user.verify_password('test_password') is True
    assert test_user.verify_password('wrong_password') is False
    
    # Test che password non sia leggibile
    with pytest.raises(AttributeError):
        _ = test_user.password

def test_user_login_logout(app, test_user):
    """Test delle funzionalità di login/logout"""
    with app.test_request_context():
        with app.test_client() as client:
            # Verifica che l'utente non sia loggato inizialmente
            assert not current_user.is_authenticated
            
            # Test login
            login_user(test_user)
            assert current_user.is_authenticated
            assert current_user.id == test_user.id
            
            # Test logout
            logout_user()
            assert not current_user.is_authenticated

def test_user_loader(app, test_user):
    """Test della funzione user_loader"""
    with app.test_request_context():
        from app.core.auth import load_user
        
        # Test caricamento utente valido
        loaded_user = load_user(test_user.id)
        assert loaded_user is not None
        assert loaded_user.id == test_user.id
        
        # Test caricamento utente non esistente
        assert load_user(999999) is None

def test_user_to_dict(test_user):
    """Test del metodo to_dict"""
    user_dict = test_user.to_dict()
    
    # Verifica che i campi sensibili non siano inclusi
    assert '_password' not in user_dict
    assert 'password' not in user_dict
    
    # Verifica che i campi principali siano presenti
    assert user_dict['email'] == 'test@example.com'
    assert user_dict['username'] == 'test_user'
    assert user_dict['role'] == 'user'
    assert user_dict['is_active'] is True

def test_user_role(test_user):
    """Test della gestione dei ruoli"""
    from app.models.user import UserRole
    
    # Test ruolo default
    assert test_user.role == UserRole.USER
    
    # Test cambio ruolo
    test_user.role = UserRole.ADMIN
    assert test_user.role == UserRole.ADMIN