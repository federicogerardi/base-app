from . import main
from flask import jsonify

@main.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "Flask API is running"
    }) 