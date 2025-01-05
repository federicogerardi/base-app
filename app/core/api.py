from flask_restx import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.controllers.api import api_ns

def init_api(app):
    """Inizializza l'API."""
    # Configura l'API
    api = Api(
        app,
        version='1.0',
        title='Flask API',
        description='API Documentation',
        doc='/api/docs',
        prefix='/api'
    )
    
    # Inizializza il rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri="memory://",
        default_limits=["2 per second"]
    )
    
    # Applica il rate limiter come decoratore
    def rate_limit_decorator(func):
        return limiter.limit("2 per second")(func)
    
    # Aggiungi il decoratore al namespace
    api_ns.decorators = [rate_limit_decorator]
    
    # Registra il namespace
    api.add_namespace(api_ns)
    
    # Gestione della documentazione Swagger
    @app.route('/api/docs/')
    def swagger_ui():
        return app.redirect('/api/docs')
    
    return api 