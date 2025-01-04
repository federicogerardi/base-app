from . import main
from flask import jsonify, current_app
from app.core.exceptions import AppException
from app.core.security import limiter

@main.route('/')
@limiter.limit("1 per second")
def index():
    current_app.logger.info("Index route accessed")
    return jsonify({
        'success': True,
        'message': 'Flask API is running'
    })

@main.route('/test-error')
@limiter.limit("5 per minute")
def test_error():
    """Test per AppException personalizzata"""
    current_app.logger.info("Test error route accessed")
    raise AppException("Questo è un errore di test", status_code=400)

@main.route('/test-exception')
def test_exception():
    """Test per errore non gestito"""
    current_app.logger.info("Test exception route accessed")
    try:
        # Generiamo un errore di esempio
        result = 1 / 0  # ZeroDivisionError
    except Exception as e:
        current_app.logger.error(f"Error in test_exception: {str(e)}")
        raise Exception("Errore di test: divisione per zero") 