import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chiavi per i test
    SECRET_KEY = os.getenv('TEST_SECRET_KEY', 'test-secret-key-123')
    JWT_SECRET_KEY = os.getenv('TEST_JWT_SECRET_KEY', 'test-jwt-key-123')
    
    # Disabilita CSRF per i test
    WTF_CSRF_ENABLED = False
    
    # Configurazioni JWT
    JWT_TOKEN_LOCATION = ['headers']
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 ora