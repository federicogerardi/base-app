import os
from pathlib import Path

class DevelopmentConfig:
    DEBUG = True
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'dev-secret-key'