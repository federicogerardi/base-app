from flask import Blueprint
from flask_login import login_required
from app.controllers.sheet_controller import SheetController

sheet = Blueprint('sheet', __name__, url_prefix='/sheet')
sheet_controller = SheetController()  # Istanziamo il controller

@sheet.route('/')
@login_required
def index():
    """Lista dei fogli"""
    return sheet_controller.index()

@sheet.route('/create')
@login_required
def create():
    """Creazione nuovo foglio"""
    return sheet_controller.create()

@sheet.route('/<int:sheet_id>')
@login_required
def view(sheet_id):
    """Visualizzazione singolo foglio"""
    return sheet_controller.view(sheet_id)
