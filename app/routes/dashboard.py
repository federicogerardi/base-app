from flask import Blueprint, render_template
from flask_login import login_required
from app.services.dashboard_service import DashboardService

# Blueprint per la dashboard
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    """Dashboard principale dell'applicazione"""
    stats = DashboardService.get_dashboard_stats()
    activities = DashboardService.get_recent_activities()
    
    return render_template('dashboard.html', 
                         stats=stats,
                         activities=activities)

# Rotte per gli sheet
@dashboard.route('/dashboard/sheet')
@login_required
def sheet_index():
    """Lista dei fogli"""
    return render_template('dashboard/sheet/index.html')

@dashboard.route('/dashboard/sheet/create')
@login_required
def sheet_create():
    """Creazione nuovo foglio"""
    return render_template('dashboard/sheet/create.html')

@dashboard.route('/dashboard/sheet/<int:sheet_id>')
@login_required
def sheet_view(sheet_id):
    """Visualizzazione singolo foglio"""
    return render_template('dashboard/sheet/view.html', sheet_id=sheet_id)