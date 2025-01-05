from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, verify_jwt_in_request,
    get_jwt, jwt_required
)
from datetime import timedelta
from flask_login import LoginManager
from app.models import User

jwt = JWTManager()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_auth(app):
    """Inizializza il sistema di autenticazione"""
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # specificheremo questa route più tardi
    login_manager.login_message = 'Per favore effettua il login per accedere a questa pagina.'
    login_manager.login_message_category = 'warning'
    
    # Gestione errori JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'success': False,
            'message': 'Il token è scaduto'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'success': False,
            'message': 'Token non valido'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return jsonify({
            'success': False,
            'message': 'Accesso non autorizzato'
        }), 401

def auth_required(f):
    """Decoratore per proteggere le route che richiedono autenticazione"""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            current_user = get_jwt_identity()
            current_app.logger.info(f"Accesso autorizzato per l'utente: {current_user}")
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.warning(f"Tentativo di accesso non autorizzato: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Accesso non autorizzato'
            }), 401
    return decorated

class AuthManager:
    @staticmethod
    def create_token(user_id: str, expires_delta: timedelta = None) -> str:
        """Crea un nuovo token JWT"""
        if expires_delta is None:
            expires_delta = timedelta(days=1)
        return create_access_token(
            identity=user_id,
            expires_delta=expires_delta
        )
    
    @staticmethod
    def get_current_user() -> str:
        """Ottiene l'identità dell'utente corrente"""
        return get_jwt_identity()
    
    @staticmethod
    def get_token_data() -> dict:
        """Ottiene i dati completi del token"""
        return get_jwt()
