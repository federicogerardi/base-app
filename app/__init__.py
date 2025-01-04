from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from app.config import config_by_name
from app.core.database import init_db
from app.core.auth import init_auth
from app.core.security import init_security
from app.core.api import init_api
from app.core.exceptions import AppException
from app.core.logger import setup_logger
from app.controllers import register_blueprints
from app.core.template_helpers import init_template_helpers

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)
    
    # Configurazione
    app.config.from_object(config_by_name[config_name])
    
    # Setup logger
    logger = setup_logger(app)
    
    # Inizializzazione componenti
    init_db(app)
    init_auth(app)
    init_security(app)
    
    # Inizializza l'API
    api = init_api(app)
    
    # Registra gli altri blueprints
    register_blueprints(app)
    
    init_template_helpers(app)
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return jsonify({
            'success': False,
            'message': 'Not Found'
        }), 404
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle any uncaught exception."""
        if isinstance(error, AppException):
            return jsonify({
                'success': False,
                'message': str(error)
            }), error.status_code
            
        if isinstance(error, HTTPException):
            return jsonify({
                'success': False,
                'message': error.description
            }), error.code
        
        app.logger.error(f"Unhandled error: {str(error)}")
        return jsonify({
            'success': False,
            'message': 'Internal Server Error'
        }), 500
    
    return app
