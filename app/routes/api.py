from flask import Blueprint
from app.controllers.api import APIController

api_bp = Blueprint('api', __name__)
api_controller = APIController()

@api_bp.route('/')
def index():
    """Route principale dell'API"""
    return api_controller.get()

@api_bp.route('/test-error')
def test_error():
    """Route di test per gli errori"""
    return api_controller.handle_error("Questo è un errore di test", 400) 