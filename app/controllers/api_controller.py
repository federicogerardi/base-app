"""
Nuovo controller per le API, spostato da routes.py
"""
from flask import current_app
from app.core.exceptions import AppException

class APIController:
    @staticmethod
    def index():
        """Gestisce l'endpoint principale dell'API"""
        current_app.logger.info("Index route accessed")
        return {
            'success': True,
            'message': 'Flask API is running'
        }

    @staticmethod
    def test_error():
        """Test della gestione errori"""
        current_app.logger.info("Test error route accessed")
        raise AppException("Questo è un errore di test", status_code=400) 