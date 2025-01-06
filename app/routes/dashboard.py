from flask import Blueprint
from flask_login import login_required
from app.controllers.dashboard import DashboardController

dashboard = Blueprint('dashboard', __name__)

dashboard_controller = DashboardController()

@dashboard.route('/dashboard')
@login_required
def index():
    return dashboard_controller.index()

@dashboard.route('/dashboard/users')
@login_required
def users():
    return dashboard_controller.users()