from .web_routes import web

def register_blueprints(app):
    """Registra tutti i blueprints dell'applicazione"""
    # Registra solo le route web
    app.register_blueprint(web)
