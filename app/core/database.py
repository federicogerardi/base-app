from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager
from typing import Type, List, Optional, Any
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import current_app

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

class DatabaseError(Exception):
    """Eccezione base per errori del database"""
    pass

class DatabaseManager:
    @staticmethod
    @contextmanager
    def session():
        session = db.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add(model: db.Model) -> db.Model:
        """Aggiunge un modello al database"""
        try:
            db.session.add(model)
            db.session.commit()
            return model
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante l'aggiunta del modello: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def update(model: db.Model, **kwargs) -> db.Model:
        """Aggiorna un modello esistente"""
        try:
            # Verifica che tutti i campi esistano prima dell'aggiornamento
            valid_fields = [column.key for column in model.__table__.columns]
            invalid_fields = [field for field in kwargs.keys() if field not in valid_fields]
            
            if invalid_fields:
                raise DatabaseError(f"Campi non validi: {', '.join(invalid_fields)}")
            
            for key, value in kwargs.items():
                setattr(model, key, value)
            
            db.session.add(model)
            db.session.commit()
            return model
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante l'aggiornamento del modello: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def delete(model: db.Model) -> None:
        """Elimina un modello dal database"""
        try:
            db.session.delete(model)
            db.session.commit()
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante l'eliminazione del modello: {str(e)}")
            db.session.rollback()
            raise

    @staticmethod
    def get_by_id(model_class: Type[db.Model], id: Any) -> Optional[db.Model]:
        """Recupera un modello per ID"""
        try:
            return db.session.get(model_class, id)
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante il recupero del modello: {str(e)}")
            raise

    @staticmethod
    def get_all(model_class: Type[db.Model]) -> List[db.Model]:
        """Recupera tutti i record di un modello"""
        try:
            return db.session.query(model_class).all()
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante il recupero dei modelli: {str(e)}")
            raise

    @staticmethod
    def filter_by(model_class: Type[db.Model], **kwargs) -> List[db.Model]:
        """Filtra i record in base ai criteri specificati"""
        try:
            return db.session.query(model_class).filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            current_app.logger.error(f"Errore durante il filtraggio dei modelli: {str(e)}")
            raise
