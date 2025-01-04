import os
from pathlib import Path

class DevelopmentConfig:
    # Debug e ambiente
    DEBUG = bool(int(os.getenv('FLASK_DEBUG', '0')))
    TESTING = False
    
    # Directory di base
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    # Database
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sicurezza
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Rate Limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"
    
    # Logging
    LOG_LEVEL = "DEBUG"