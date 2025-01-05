from flask import Blueprint, render_template
from flask_login import login_required
from app.services.dashboard_service import DashboardService

# Modifica: rimuovi il prefisso dal blueprint
dashboard = Blueprint('dashboard', __name__)

# Modifica: mantieni il percorso completo nella route
@dashboard.route('/dashboard')
@login_required
def index():
    """Dashboard principale dell'applicazione"""
    stats = DashboardService.get_dashboard_stats()
    activities = DashboardService.get_recent_activities()
    
    return render_template('dashboard.html', 
                         stats=stats,
                         activities=activities) 