import os

class ProductionConfig:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/prod_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'prod-secret-key')  # Meglio usare una variabile d'ambiente