import pytest
from app import create_app
from app.core.database import db
from app.models.base import BaseModel
from app.core.auth import AuthManager
from dotenv import load_dotenv

# Modello di test spostato qui
class TestModel(BaseModel):
    """Modello utilizzato solo per i test"""
    __tablename__ = 'test_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@pytest.fixture
def app():
    """Fixture dell'applicazione per i test"""
    load_dotenv()
    
    app = create_app('testing')
    
    # Configurazioni specifiche per i test
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SERVER_NAME'] = 'localhost'  # Importante per url_for
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Crea un client di test"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Crea un runner per i comandi CLI"""
    return app.test_cli_runner()

@pytest.fixture
def test_model():
    """Fixture per accedere al modello di test"""
    return TestModel

@pytest.fixture
def auth_headers(app):
    """Fixture per headers di autenticazione"""
    with app.app_context():
        token = AuthManager.create_token('test_user')
        return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def authenticated_client(client, auth_headers):
    """Client già autenticato per i test"""
    def _make_request(*args, **kwargs):
        kwargs['headers'] = {**kwargs.get('headers', {}), **auth_headers}
        return client.get(*args, **kwargs)
    return _make_request
