from flask import Blueprint
from flask_login import login_required
from app.controllers.dashboard import DashboardController
from app.core.decorators import admin_required

dashboard = Blueprint('dashboard', __name__)

dashboard_controller = DashboardController()

@dashboard.route('/dashboard')
@admin_required
def index():
    return dashboard_controller.index()

@dashboard.route('/dashboard/users')
@admin_required
def users():
    return dashboard_controller.users()