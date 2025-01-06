from app.controllers.base import BaseController
from app.services.dashboard_service import DashboardService
from app.core.decorators import admin_required

class DashboardController(BaseController):
    def __init__(self):
        super().__init__()
    
    @admin_required
    def index(self):
        """Logica per la dashboard principale"""
        try:
            stats = DashboardService.get_dashboard_stats()
            activities = DashboardService.get_recent_activities()
            return self.render_view('dashboard.html', 
                                  stats=stats,
                                  activities=activities,
                                  title="Dashboard")
        except Exception as e:
            return self.handle_error(str(e)) 
    
    @admin_required
    def users(self):
        """Logica per la gestione degli utenti"""
        try:
            users = DashboardService.get_all_users()
            return self.render_view('users.html', title="Gestione Utenti", users=users)
        except Exception as e:
            return self.handle_error(str(e)) 
