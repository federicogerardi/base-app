from flask import Flask, jsonify
from flask_cors import CORS
from app.config import config_by_name
from app.core.database import init_db
from app.core.auth import init_auth
from app.core.exceptions import AppException
from app.core.logger import setup_logger
from werkzeug.exceptions import HTTPException

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
    
    # Registrazione blueprints
    from app.controllers import register_blueprints
    register_blueprints(app)
    
    # Log dell'avvio dell'applicazione
    logger.info(f"Application started in {config_name} mode")

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle any uncaught exception."""
        try:
            # AppException
            if isinstance(error, AppException):
                logger.warning(f"AppException: {str(error)}")
                return jsonify({
                    'success': False,
                    'message': str(error)
                }), error.status_code

            # HTTPException (404, etc)
            if isinstance(error, HTTPException):
                logger.info(f"HTTP {error.code}: {error.description}")
                return jsonify({
                    'success': False,
                    'message': error.description
                }), error.code

            # Errori non gestiti
            logger.error(f"Unhandled error: {str(error)}")
            
            response = {
                'success': False,
                'message': 'Internal Server Error'
            }
            
            if app.debug:
                response['debug'] = {
                    'error': str(error),
                    'type': error.__class__.__name__
                }
            
            return jsonify(response), 500
            
        except Exception as e:
            logger.error(f"Error in error handler: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Internal Server Error'
            }), 500
    
    return app
