from flask import Flask
from flask_cors import CORS
from app.config import config_by_name
from app.core.database import init_db
from app.core.auth import init_auth
from app.core.exceptions import AppException

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)
    
    # Configurazione
    app.config.from_object(config_by_name[config_name])
    
    # Inizializzazione componenti
    init_db(app)
    init_auth(app)
    
    # Registrazione blueprints
    from app.controllers import register_blueprints
    register_blueprints(app)
    
    # Gestione errori
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return {'message': error.message}, error.status_code
    
    return app
