from datetime import datetime, timedelta
from app.models import User

class DashboardService:
    @staticmethod
    def get_dashboard_stats():
        """Recupera le statistiche per la dashboard"""
        return {
            'total_users': User.query.count(),
            'active_users': User.query.filter(User.last_login > datetime.utcnow() - timedelta(days=7)).count(),
            'pending_users': 0,  # Placeholder
            'growth': '+12%'  # Placeholder
        }
    
    @staticmethod
    def get_recent_activities():
        """Recupera le attività recenti"""
        # Per ora restituiamo dati statici
        return [
            {
                'icon': 'user-plus',
                'text': 'Nuovo utente registrato',
                'time': '2 minuti fa',
                'type': 'success'
            },
            {
                'icon': 'tasks',
                'text': 'Aggiornamento completato',
                'time': '1 ora fa',
                'type': 'primary'
            },
            {
                'icon': 'exclamation-triangle',
                'text': 'Avviso di sistema',
                'time': '3 ore fa',
                'type': 'warning'
            }
        ] 