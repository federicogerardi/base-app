from datetime import datetime, timedelta
from app.models import User
from app.core.database import DatabaseManager
from app.models.user import UserRole

class DashboardService:
    @staticmethod
    def get_all_users():
        """Recupera tutti gli utenti dal database"""
        return DatabaseManager.get_all(User)

    @staticmethod
    def create_user(username, email, password, role):
        """Crea un nuovo utente"""
        try:
            new_user = User(
                username=username,
                email=email,
                password=password,
                role=UserRole[role.upper()]
            )
            return DatabaseManager.add(new_user)
        except Exception as e:
            raise Exception(f"Errore durante la creazione dell'utente: {str(e)}")

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