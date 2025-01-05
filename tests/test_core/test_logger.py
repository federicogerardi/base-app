from app.core.logger import setup_logger

def test_logger_configuration(app):
    """Test della configurazione del logger"""
    logger = setup_logger(app)
    assert logger is not None
    assert len(logger._core.handlers) > 0  # Verifica che ci siano gestori configurati 