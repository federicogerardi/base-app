import os

class Config:
    # ... existing config ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-chiave-segreta-molto-lunga-e-complessa' 