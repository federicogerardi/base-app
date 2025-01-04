from app.core.template_helpers import safe_url_for
from flask import Blueprint

def test_safe_url_for(app):
    """Test dell'helper safe_url_for"""
    # Crea un blueprint di test
    test_bp = Blueprint('test_web', __name__)
    
    @test_bp.route('/')
    def index():
        return 'Test Index'
    
    # Registra il blueprint
    app.register_blueprint(test_bp, url_prefix='/')
    
    # Test con un contesto di richiesta
    with app.test_request_context('/'):
        # Test route esistente
        assert safe_url_for('test_web.index') == '/'
        
        # Test route inesistente
        assert safe_url_for('non.esistente') == '#'
        
        # Test con parametri
        assert safe_url_for('test_web.index', param='test') == '/?param=test' 