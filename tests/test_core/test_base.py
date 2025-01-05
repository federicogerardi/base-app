import pytest
from flask import Flask
from app.controllers.base import BaseController
from app.core.database import db
from app.core.exceptions import AppException

# Definizione del modello fuori dalla fixture
class TestModel(db.Model):
    __tablename__ = 'test_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

@pytest.fixture
def app():
    """Create application for the tests."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inizializza il database
    db.init_app(app)
    
    # Crea un contesto dell'applicazione
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_model():
    """Return the test model class."""
    return TestModel

def test_base_controller(app, test_model):
    """Test del controller base"""
    with app.app_context():
        controller = BaseController(model_class=test_model)
        
        # Test json_response
        response, status = controller.json_response({'test': 'data'})
        assert response.json['success'] is True
        assert response.json['data']['test'] == 'data'
        assert status == 200
        
        # Test render_view
        with pytest.raises(Exception):  # Flask non può renderizzare template in test
            controller.render_view('index.html', test_var='value')
        
        # Test handle_error
        with pytest.raises(AppException) as exc_info:
            controller.handle_error("Test error", 400)
        assert str(exc_info.value) == "Test error"
        assert exc_info.value.status_code == 400

def test_base_controller_model_class(app, test_model):
    """Test inizializzazione controller con model_class"""
    with app.app_context():
        # Test con model_class valido
        controller = BaseController(model_class=test_model)
        assert controller.model_class == test_model
        
        # Test senza model_class (dovrebbe essere valido)
        controller = BaseController()
        assert controller.model_class is None 