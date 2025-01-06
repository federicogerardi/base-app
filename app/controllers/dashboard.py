from app.controllers.base import BaseController
from app.services.dashboard_service import DashboardService

class DashboardController(BaseController):
    def __init__(self):
        super().__init__()
    
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
    
    def users(self):
        """Logica per la gestione degli utenti"""
        try:
            return self.render_view('users.html', title="Gestione Utenti")
        except Exception as e:
            return self.handle_error(str(e)) 
