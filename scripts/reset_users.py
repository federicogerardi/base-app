# ATTENZIONE: Questo script cancella la tabella User e la ricrea con l'utente admin di default.

import os
import sys
from datetime import UTC, datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import User
from app.core.database import db
from werkzeug.security import generate_password_hash
from sqlalchemy import text

def reset_users():
    app = create_app()
    
    with app.app_context():
        # Aggiungi input di conferma
        confirm = input("Sei sicuro di voler resettare il database? (s/n): ")
        if confirm.lower() != 's':
            print("Operazione annullata.")
            return
        
        # Drop e ricrea la tabella User
        print("Eliminazione tabella User...")
        db.session.execute(text('DROP TABLE IF EXISTS users'))
        db.session.commit()
        db.create_all()
        print("Tabella User ricreata")
        
        # Crea l'utente admin
        admin = User(
            username='federico',
            email='federico@example.com',
            password='efefkjuieweu',
            role='ADMIN',
            created_at=datetime.now(UTC)
        )
        
        # Salva nel database
        db.session.add(admin)
        db.session.commit()
        
        # Verifica
        user = User.query.first()
        print("\nUtente admin creato:")
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Created: {user.created_at}")

if __name__ == '__main__':
    reset_users() 