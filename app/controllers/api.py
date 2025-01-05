"""
Controller per le API
"""
from flask_restx import Resource
from flask import current_app, jsonify
from app.controllers.base import BaseController

class APIController(Resource, BaseController):
    def __init__(self, api=None, *args, **kwargs):
        """
        Inizializza il controller API
        :param api: L'istanza dell'API Flask-RESTx
        """
        Resource.__init__(self, api, *args, **kwargs)
        BaseController.__init__(self)
    
    def get(self):
        """Gestisce le richieste GET all'endpoint principale dell'API"""
        current_app.logger.info("API GET request received")
        return {
            'success': True,
            'message': 'Flask API is running'
        }
    
    def post(self):
        """Gestisce le richieste POST all'endpoint principale dell'API"""
        current_app.logger.info("API POST request received")
        return {
            'success': True,
            'message': 'POST request processed successfully'
        }

    def handle_error(self, message, status_code=400):
        """Gestisce gli errori dell'API"""
        current_app.logger.warning(f"API error: {message}")
        return {
            'success': False,
            'message': message
        }, status_code 