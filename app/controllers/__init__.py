from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes

def register_blueprints(app):
    app.register_blueprint(main)
