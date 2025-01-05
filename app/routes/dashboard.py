from flask import Blueprint
from flask_login import login_required
from app.controllers.dashboard_controller import DashboardController

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    """Dashboard principale dell'applicazione"""
    return DashboardController.index()