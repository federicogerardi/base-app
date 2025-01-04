#!/bin/bash

echo "La struttura verrà creata in: $(pwd)"
read -p "Vuoi procedere? (si/no): " risposta

risposta=$(echo "$risposta" | tr '[:upper:]' '[:lower:]')

if [ "$risposta" != "si" ] && [ "$risposta" != "s" ]; then
    echo "Operazione annullata"
    exit 1
fi

# Creazione della struttura principale
mkdir -p app/{config,core,models,controllers,views/templates,static/{css,js,img},utils}
mkdir -p tests/test_core

# Creazione di app/config/__init__.py
cat > app/config/__init__.py << 'EOL'
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
EOL

# Creazione di app/models/base.py
cat > app/models/base.py << 'EOL'
from app.core.database import db

class BaseModel(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())
EOL

# Creazione di app/controllers/base.py
cat > app/controllers/base.py << 'EOL'
from flask import Blueprint, jsonify

class BaseController:
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self):
        items = self.model_class.query.all()
        return jsonify([item.to_dict() for item in items])
EOL

# Creazione di app/core/exceptions.py
cat > app/core/exceptions.py << 'EOL'
class AppException(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
EOL

# Creazione di app/core/database.py
cat > app/core/database.py << 'EOL'
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

class DatabaseManager:
    @staticmethod
    @contextmanager
    def session():
        session = db.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add(model):
        with DatabaseManager.session() as session:
            session.add(model)
            return model
    
    @staticmethod
    def delete(model):
        with DatabaseManager.session() as session:
            session.delete(model)
EOL

# Creazione di app/core/auth.py
cat > app/core/auth.py << 'EOL'
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, verify_jwt_in_request
)

jwt = JWTManager()

def init_auth(app):
    jwt.init_app(app)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"message": "Token non valido"}), 401
    return decorated

class AuthManager:
    @staticmethod
    def create_token(user_id):
        return create_access_token(identity=user_id)
    
    @staticmethod
    def get_current_user():
        return get_jwt_identity()
EOL

# Creazione di app/config/development.py
cat > app/config/development.py << 'EOL'
import os
from pathlib import Path

class DevelopmentConfig:
    DEBUG = True
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'dev-secret-key'
EOL

# Creazione di app/config/production.py
cat > app/config/production.py << 'EOL'
class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/prod_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'prod-secret-key'  # Da cambiare in produzione!
EOL

# Creazione di app/config/testing.py
cat > app/config/testing.py << 'EOL'
import os
from pathlib import Path

class TestingConfig:
    TESTING = True
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key'
EOL

# Aggiornamento di app/__init__.py per includere auth
cat > app/__init__.py << 'EOL'
from flask import Flask
from flask_cors import CORS
from app.config import config_by_name
from app.core.database import init_db
from app.core.auth import init_auth
from app.core.exceptions import AppException

def create_app(config_name='development'):
    app = Flask(__name__)
    CORS(app)
    
    # Configurazione
    app.config.from_object(config_by_name[config_name])
    
    # Inizializzazione componenti
    init_db(app)
    init_auth(app)
    
    # Gestione errori
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return {'message': error.message}, error.status_code
    
    return app
EOL

# Creazione del Makefile
cat > Makefile << 'EOL'
.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest tests/

run:
	flask run

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
EOL

# Creazione degli altri file vuoti
touch app/config/{development.py,production.py,testing.py}
touch app/core/{__init__.py,database.py,auth.py}
touch app/models/__init__.py
touch app/controllers/__init__.py
touch app/views/__init__.py
touch app/views/templates/base.html
touch app/utils/{__init__.py,helpers.py}
touch tests/{__init__.py,conftest.py}
touch {requirements.txt,run.py,README.md}

# Imposta i permessi di esecuzione
chmod +x run.py

# Creazione di requirements.txt
cat > requirements.txt << 'EOL'
flask==3.0.0
flask-sqlalchemy==3.1.1
flask-migrate==4.0.5
flask-cors==4.0.0
flask-jwt-extended==4.5.3
python-dotenv==1.0.0
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
flake8==7.0.0
isort==5.13.2
EOL

echo "Struttura del progetto creata con successo nella directory corrente"