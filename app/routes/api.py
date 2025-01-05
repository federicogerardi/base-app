"""
Sposta qui le rotte API da controllers/routes.py
"""
from flask import Blueprint
from app.controllers.api_controller import APIController

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def index():
    return APIController.index()

@api_bp.route('/test-error')
def test_error():
    return APIController.test_error() 