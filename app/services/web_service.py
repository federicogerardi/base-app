class WebService:
    @staticmethod
    def get_home_data():
        """Recupera i dati per la homepage"""
        return {
            'welcome_message': 'Flask App Starter Kit',
            'features': [
                {
                    'title': 'Dashboard',
                    'description': 'Accedi alle tue statistiche',
                    'icon': 'chart-line'
                },
                {
                    'title': 'Gestione Utenti',
                    'description': 'Amministra gli account',
                    'icon': 'users'
                },
                {
                    'title': 'Impostazioni',
                    'description': 'Configura la tua esperienza',
                    'icon': 'cog'
                }
            ]
        } 