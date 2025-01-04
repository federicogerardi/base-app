"""
Modulo di inizializzazione dell'applicazione Flask.

Questo modulo contiene la funzione `create_app` che configura e restituisce
un'istanza dell'app Flask. Include l'inizializzazione di componenti core come
il database, l'autenticazione, la sicurezza, e la registrazione dei blueprint.
Gestisce anche gli errori comuni come 404 e altre eccezioni generiche.
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
from app.controllers import register_blueprints
from app.core.template_helpers import init_template_helpers

def create_app(config_name='development'):
    """Crea e configura l'app Flask."""
    app = Flask(__name__)
    CORS(app)  # Abilita CORS per tutte le route
    
    # Carica la configurazione basata sul nome fornito
    app.config.from_object(config_by_name[config_name])
    
    # Configura il logger dell'applicazione
    logger = setup_logger(app)
    
    # Inizializza i componenti core
    init_db(app)  # Inizializza il database
    init_auth(app)  # Inizializza l'autenticazione
    init_security(app)  # Inizializza la sicurezza
    
    # Inizializza l'API e registra i blueprint
    api = init_api(app)
    register_blueprints(app)
    
    # Inizializza gli helper per i template
    init_template_helpers(app)
    
    # Gestione degli errori
    @app.errorhandler(404)
    def not_found_error(error):
        """Gestisce gli errori 404."""
        return jsonify({
            'success': False,
            'message': 'Not Found'
        }), 404
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Gestisce le eccezioni non catturate."""
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
