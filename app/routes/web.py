from flask import Blueprint
from app.controllers.web import WebController

web = Blueprint('web', __name__)

web_controller = WebController()

@web.route('/')
def index():
    return web_controller.index()

