from app.controllers.base import BaseController
from app.services.dashboard_service import DashboardService
from app.core.decorators import admin_required
from flask import request, jsonify
from app.models.user import User, UserRole
from app.core.database import DatabaseManager
import traceback
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email

class AddUserForm(FlaskForm):
    csrf_token = HiddenField()
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Ruolo', choices=[('user', 'Utente'), ('admin', 'Amministratore')])

class DashboardController(BaseController):
    def __init__(self):
        super().__init__()
    
    @admin_required
    def index(self):
        """Logica per la dashboard principale.
        
        Recupera le statistiche e le attività recenti da visualizzare nella dashboard.
        """
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
        """Logica per la gestione degli utenti.
        
        Recupera la lista degli utenti e prepara il modulo per aggiungere un nuovo utente.
        """
        try:
            users = DashboardService.get_all_users()
            form = AddUserForm()
            return self.render_view('users.html', 
                                  title="Gestione Utenti", 
                                  users=users,
                                  form=form)
        except Exception as e:
            return self.handle_error(str(e)) 

    @admin_required
    def add_user(self):
        """Logica per aggiungere un nuovo utente.
        
        Valida i dati dell'utente e lo aggiunge al database. 
        Richiede che la richiesta sia in formato JSON.
        """
        try:
            if not request.is_json:
                return jsonify({"error": "Richiesta non valida: Content-Type deve essere application/json"}), 400

            data = request.get_json()
            
            # Validazione dei dati
            required_fields = ['username', 'email', 'password', 'role']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({"error": f"Campo {field} mancante"}), 400

            # Creazione nuovo utente
            new_user = User(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role=UserRole[data['role'].upper()]
            )

            # Aggiunta dell'utente al database
            DatabaseManager.add(new_user)

            return jsonify({
                "message": "Utente aggiunto con successo!",
                "user": new_user.to_dict()
            }), 201

        except KeyError as e:
            print(f"KeyError: {str(e)}")
            return jsonify({"error": f"Ruolo non valido: {str(e)}"}), 400
        except Exception as e:
            print(f"Errore: {str(e)}")
            print(traceback.format_exc())  # Stampa il traceback completo
            return jsonify({"error": str(e)}), 400 
