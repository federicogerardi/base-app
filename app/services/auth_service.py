from typing import Optional, Tuple
from flask_login import login_user, logout_user
from app.models import User
from app.core.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime, UTC

class AuthService:
    @staticmethod
    def register_user(email: str, username: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Registra un nuovo utente
        Returns: (success, message, user)
        """
        try:
            if User.query.filter_by(email=email).first():
                return False, "Email già registrata", None
                
            if User.query.filter_by(username=username).first():
                return False, "Username già in uso", None

            user = User(
                email=email,
                username=username
            )
            user.password = password  # Viene hashata automaticamente
            
            db.session.add(user)
            db.session.commit()
            
            return True, "Registrazione completata con successo", user
            
        except Exception as e:
            current_app.logger.error(f"Errore durante la registrazione: {str(e)}")
            db.session.rollback()
            return False, f"Errore durante la registrazione: {str(e)}", None

    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Autentica un utente
        Returns: (success, message, user)
        """
        try:
            user = User.query.filter_by(email=email).first()
            
            print(f"Login attempt for email: {email}")
            print(f"User found: {user is not None}")
            
            if user and user.check_password(password):
                login_user(user, remember=True)
                user.last_login = datetime.now(UTC)
                db.session.commit()
                return True, "Login effettuato con successo", user
            
            return False, "Email o password non validi", None
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False, "Errore durante il login", None

    @staticmethod
    def logout() -> Tuple[bool, str]:
        """
        Effettua il logout dell'utente
        Returns: (success, message)
        """
        try:
            logout_user()
            return True, "Logout effettuato con successo"
        except Exception as e:
            return False, f"Errore durante il logout: {str(e)}" 