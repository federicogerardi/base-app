from app.core.database import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC
from enum import Enum
from flask_login import UserMixin

class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(BaseModel, UserMixin):
    """Modello per la gestione degli utenti"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    _password = db.Column('password', db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    last_login = db.Column(db.DateTime)

    @property
    def password(self):
        """Getter per la password"""
        return self._password

    @password.setter
    def password(self, plain_password):
        """Setter per la password che la cripta automaticamente"""
        self._password = generate_password_hash(plain_password)

    def check_password(self, password):
        """Verifica la password"""
        return check_password_hash(self._password, password)

    def update_last_login(self):
        """Aggiorna il timestamp dell'ultimo login"""
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        """Converte l'utente in dizionario (escludendo dati sensibili)"""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role.value,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }