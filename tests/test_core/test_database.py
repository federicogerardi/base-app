from app.core.database import db

def test_database_operations(app, test_model):
    """Test delle operazioni base del database"""
    # Verifica ambiente di test
    assert app.config['TESTING']
    assert ':memory:' in app.config['SQLALCHEMY_DATABASE_URI']
    
    # Crea un modello di test
    test_item = test_model(name='test')
    db.session.add(test_item)
    db.session.commit()

    # Verifica che sia stato salvato
    saved_item = test_model.query.filter_by(name='test').first()
    assert saved_item is not None
    assert saved_item.name == 'test'

    # Verifica i campi automatici
    assert saved_item.created_at is not None
    assert saved_item.updated_at is not None

def test_database_rollback(app, test_model):
    """Test del rollback delle transazioni"""
    # Verifica ambiente di test
    assert app.config['TESTING']
    assert ':memory:' in app.config['SQLALCHEMY_DATABASE_URI']
    
    try:
        # Prova a salvare un item invalido
        test_item = test_model()  # Manca il campo name (non nullable)
        db.session.add(test_item)
        db.session.commit()
        assert False, "Dovrebbe sollevare un'eccezione"
    except:
        db.session.rollback()
        # Verifica che il rollback sia avvenuto
        count = test_model.query.count()
        assert count == 0 