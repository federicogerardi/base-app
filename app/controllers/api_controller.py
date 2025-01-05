"""
Nuovo controller per le API, spostato da routes.py
"""
from app.controllers.base import BaseController
from flask import current_app

class APIController(BaseController):
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Gestisce l'endpoint principale dell'API"""
        current_app.logger.info("Index route accessed")
        return self.json_response({
            'message': 'Flask API is running'
        })

    def test_error(self):
        """Test della gestione errori"""
        current_app.logger.info("Test error route accessed")
        return self.handle_error("Questo è un errore di test", 400) 