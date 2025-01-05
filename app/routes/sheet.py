from flask import Blueprint
from flask_login import login_required
from app.controllers.sheet_controller import SheetController

sheet = Blueprint('sheet', __name__, url_prefix='/sheet')

@sheet.route('/')
@login_required
def index():
    """Lista dei fogli"""
    return SheetController.index()

@sheet.route('/create')
@login_required
def create():
    """Creazione nuovo foglio"""
    return SheetController.create()

@sheet.route('/<int:sheet_id>')
@login_required
def view(sheet_id):
    """Visualizzazione singolo foglio"""
    return SheetController.view(sheet_id)
