"""
Modulo del modello base.

Definisce la classe `BaseModel` che funge da modello astratto per tutti i
modelli dell'applicazione. Include campi comuni come timestamp di creazione
e aggiornamento.
"""

from app.core.database import db

class BaseModel(db.Model):
    """Modello base per tutti i modelli dell'applicazione."""
    __abstract__ = True
    
    # Timestamp di creazione e aggiornamento
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())
