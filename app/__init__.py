"""
Modulo di inizializzazione dell'applicazione Flask.
"""
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
from app.core.template_helpers import init_template_helpers

def create_app(config_name='development'):
    """Crea e configura l'app Flask."""
    app = Flask(__name__)
    CORS(app)
    
    # Carica la configurazione
    app.config.from_object(config_by_name[config_name])
    
    # Configura il logger
    logger = setup_logger(app)
    
    # Inizializza i componenti core
    init_db(app)
    init_auth(app)
    init_security(app)
    init_template_helpers(app)
    
    # Registra i blueprint
    register_blueprints(app)
    
    # Inizializza l'API
    api = init_api(app)
    
    # Gestione errori
    register_error_handlers(app)
    
    return app

def register_blueprints(app):
    """Registra tutti i blueprint dell'applicazione"""
    from app.routes.auth import bp as auth_bp
    from app.routes.web import web
    from app.routes.dashboard import dashboard
    from app.routes.sheet import sheet
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(web)
    app.register_blueprint(dashboard)
    app.register_blueprint(sheet)
    app.register_blueprint(api_bp)

def register_error_handlers(app):
    """Registra gli handler per gli errori"""
    @app.errorhandler(Exception)
    def handle_exception(error):
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
