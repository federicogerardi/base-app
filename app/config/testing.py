import os
from pathlib import Path

class TestingConfig:
    TESTING = True
    DEBUG = False  # Debug non necessario in testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Database in memoria
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'prod-secret-key')  # Meglio usare una variabile d'ambiente