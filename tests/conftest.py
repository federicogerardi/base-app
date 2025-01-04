import pytest
from app import create_app
from app.core.database import db
from app.models.base import BaseModel

# Modello di test spostato qui
class TestModel(BaseModel):
    """Modello utilizzato solo per i test"""
    __tablename__ = 'test_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@pytest.fixture
def app():
    """Crea un'istanza dell'applicazione per i test"""
    app = create_app('testing')
    
    # Verifica che siamo in ambiente di test
    assert app.config['TESTING'] == True
    assert ':memory:' in app.config['SQLALCHEMY_DATABASE_URI']
    
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
