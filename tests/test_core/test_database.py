import pytest
from app.core.database import db, DatabaseManager, DatabaseError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def test_database_operations(app, test_model):
    """Test delle operazioni base del database"""
    with app.app_context():
        # Test add
        test_item = test_model(name='test')
        saved_item = DatabaseManager.add(test_item)
        assert saved_item.id is not None
        assert saved_item.name == 'test'

        # Test get_by_id
        retrieved_item = DatabaseManager.get_by_id(test_model, saved_item.id)
        assert retrieved_item is not None
        assert retrieved_item.id == saved_item.id
        assert retrieved_item.name == 'test'

        # Test update
        updated_item = DatabaseManager.update(retrieved_item, name='updated')
        assert updated_item.name == 'updated'

        # Test get_all
        all_items = DatabaseManager.get_all(test_model)
        assert len(all_items) == 1
        assert all_items[0].name == 'updated'

        # Test filter_by
        filtered_items = DatabaseManager.filter_by(test_model, name='updated')
        assert len(filtered_items) == 1
        assert filtered_items[0].id == saved_item.id

        # Test delete
        DatabaseManager.delete(saved_item)
        assert DatabaseManager.get_by_id(test_model, saved_item.id) is None

def test_database_error_handling(app, test_model):
    """Test della gestione degli errori del database"""
    with app.app_context():
        # Test add con modello invalido
        with pytest.raises(IntegrityError):
            invalid_item = test_model()  # Manca il campo name (non nullable)
            DatabaseManager.add(invalid_item)

        # Test update con valori invalidi
        test_item = test_model(name='test')
        DatabaseManager.add(test_item)
        with pytest.raises(DatabaseError):
            DatabaseManager.update(test_item, non_existent_field='value')

        # Test update con valori validi
        updated_item = DatabaseManager.update(test_item, name='updated')
        assert updated_item.name == 'updated'

def test_database_session_management(app, test_model):
    """Test della gestione delle sessioni del database"""
    with app.app_context():
        # Test del commit automatico
        test_item = test_model(name='test')
        DatabaseManager.add(test_item)
        
        # Verifica che il commit sia avvenuto
        saved_item = DatabaseManager.get_by_id(test_model, test_item.id)
        assert saved_item is not None
        assert saved_item.name == 'test'

        # Test del rollback automatico
        try:
            invalid_item = test_model()  # Invalido (manca name)
            DatabaseManager.add(invalid_item)
        except IntegrityError:
            pass
        
        # Verifica che il rollback sia avvenuto
        count = DatabaseManager.get_all(test_model)
        assert len(count) == 1  # Solo il primo item valido 