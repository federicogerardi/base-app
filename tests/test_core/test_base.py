import pytest
from app.controllers.base import BaseController
from app.models.base import BaseModel

def test_base_controller(test_model):
    """Test del controller base"""
    # Usa il test_model come model_class
    controller = BaseController(model_class=test_model)
    
    # Test metodi base
    response = controller.index()
    assert response['success'] == True
    assert 'message' in response
    
    response = controller.health_check()
    assert response['status'] == 'healthy'
    assert response['model'] == test_model.__name__
    
    # Test gestione errori
    response = controller.handle_error("Test error")
    assert response['success'] == False
    assert 'Test error' in response['message']

def test_base_controller_validation():
    """Test validazione del controller base"""
    # Test inizializzazione senza model_class
    with pytest.raises(TypeError) as exc_info:
        BaseController()
    assert "model_class è richiesto" in str(exc_info.value)
    
    # Test con classe non-Model
    with pytest.raises(ValueError) as exc_info:
        BaseController(model_class=str)
    assert "model_class deve essere una sottoclasse di BaseModel" in str(exc_info.value) 