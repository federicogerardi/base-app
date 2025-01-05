import os
from datetime import timedelta

class DevelopmentConfig:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev_jwt_secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
    # Debug
    DEBUG = True