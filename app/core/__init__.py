from flask import Flask
from .database import init_db
from .auth import init_auth

def create_app(config_name="development"):
    app = Flask(__name__, 
                template_folder='../templates')
    
    # Configurazione
    if isinstance(config_name, str):
        app.config.from_object(f'app.config.{config_name}.{config_name.capitalize()}Config')
    else:
        app.config.from_object(config_name)
    
    # Inizializzazioni
    init_db(app)
    init_auth(app)
    
    # Route di base
    @app.route('/')
    def index():
        return 'Home Page'
    
    # Registrazione blueprints
    with app.app_context():
        from app.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        
    return app
