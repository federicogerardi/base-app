from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from contextlib import contextmanager

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)

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
    def add(model):
        with DatabaseManager.session() as session:
            session.add(model)
            return model
    
    @staticmethod
    def delete(model):
        with DatabaseManager.session() as session:
            session.delete(model)
