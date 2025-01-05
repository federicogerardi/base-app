from flask_restx import Api
from app.controllers.api import APIController

def init_api(app):
    """Inizializza l'API."""
    api = Api(
        app,
        version='1.0',
        title='Flask API',
        description='API Documentation',
        doc='/api/docs',
        prefix='/api'
    )
    
    # Crea un namespace per le API
    ns = api.namespace('', description='API operations')
    
    # Registra i controller
    ns.add_resource(APIController, '/')
    
    return api 