from flask import current_app
from app.core.exceptions import AppException
from app.core.security import limiter
from app.core.api import main_ns, success_model, error_model
from flask_restx import Resource

@main_ns.route('/')
class IndexResource(Resource):
    @main_ns.doc('index', description='Endpoint principale dell\'API')
    @main_ns.response(200, 'Success', success_model)
    @main_ns.response(429, 'Too Many Requests', error_model)
    @limiter.limit("1 per second")
    def get(self):
        """Endpoint principale dell'API
        
        Returns:
            Un messaggio di benvenuto con status success
        """
        current_app.logger.info("Index route accessed")
        return {
            'success': True,
            'message': 'Flask API is running'
        }

@main_ns.route('/test-error')
class TestErrorResource(Resource):
    @main_ns.doc('test_error', description='Test della gestione errori')
    @main_ns.response(400, 'Bad Request', error_model)
    @main_ns.response(429, 'Too Many Requests', error_model)
    @limiter.limit("5 per minute")
    def get(self):
        """Test endpoint per la gestione degli errori
        
        Raises:
            AppException: Solleva un errore di test
        """
        current_app.logger.info("Test error route accessed")
        raise AppException("Questo è un errore di test", status_code=400)