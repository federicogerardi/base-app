import os
from pathlib import Path

class TestingConfig:
    TESTING = True
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key'