from flask import Blueprint
from flask_restx import Api, Resource, fields

# Crea un blueprint per l'API
blueprint = Blueprint('api_v1', __name__, url_prefix='/api')

# Inizializza l'API con la documentazione
api = Api(blueprint,
    title='Flask Starter API',
    version='1.0',
    description='A Flask REST API starter kit',
    doc='/docs/',
    specs_url='/swagger.json'
)

# Namespace per organizzare le API
main_ns = api.namespace('main', 
    description='Main operations'
)

# Modelli per la documentazione
error_model = api.model('Error', {
    'success': fields.Boolean(default=False),
    'message': fields.String(required=True)
})

success_model = api.model('Success', {
    'success': fields.Boolean(default=True),
    'message': fields.String(required=True)
})

# Importa i controllers qui per evitare import circolari
def init_api(app):
    """Inizializza l'API e la documentazione"""
    from app.controllers import routes  # Importa le route qui
    app.register_blueprint(blueprint)
    return api 