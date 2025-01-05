from flask import Blueprint
from app.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET'])
def login():
    """Mostra la pagina di login"""
    return AuthController.login()

@bp.route('/login', methods=['POST'])
def login_post():
    """Gestisce il processo di login"""
    return AuthController.login_post()

@bp.route('/register', methods=['GET'])
def register():
    """Mostra la pagina di registrazione"""
    return AuthController.register()

@bp.route('/register', methods=['POST'])
def register_post():
    """Gestisce il processo di registrazione"""
    return AuthController.register_post()

@bp.route('/logout')
def logout():
    """Gestisce il processo di logout"""
    return AuthController.logout() 