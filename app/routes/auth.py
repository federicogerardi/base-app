from flask import Blueprint
from app.controllers.auth_controller import AuthController

bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_controller = AuthController()

@bp.route('/login', methods=['GET'])
def login():
    """Mostra la pagina di login"""
    return auth_controller.login()

@bp.route('/login', methods=['POST'])
def login_post():
    """Gestisce il processo di login"""
    return auth_controller.login_post()

@bp.route('/register', methods=['GET'])
def register():
    """Mostra la pagina di registrazione"""
    return auth_controller.register()

@bp.route('/register', methods=['POST'])
def register_post():
    """Gestisce il processo di registrazione"""
    return auth_controller.register_post()

@bp.route('/logout')
def logout():
    """Gestisce il processo di logout"""
    return auth_controller.logout() 