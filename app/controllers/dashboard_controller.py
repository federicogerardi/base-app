from app.services.dashboard_service import DashboardService
from flask import render_template

class DashboardController:
    @staticmethod
    def index():
        """Logica per la dashboard principale"""
        stats = DashboardService.get_dashboard_stats()
        activities = DashboardService.get_recent_activities()
        return render_template('dashboard.html', 
                             stats=stats,
                             activities=activities) 