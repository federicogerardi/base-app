from flask import Blueprint
from flask_login import login_required
from app.controllers.dashboard_controller import DashboardController

dashboard = Blueprint('dashboard', __name__)

dashboard_controller = DashboardController()

@dashboard.route('/dashboard')
@login_required
def index():
    return dashboard_controller.index()