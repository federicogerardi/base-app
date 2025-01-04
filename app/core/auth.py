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
