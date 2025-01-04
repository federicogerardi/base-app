from app.models.base import BaseModel
from typing import Type, Dict, Any

class BaseController:
    def __init__(self, model_class: Type[BaseModel] = None):
        if model_class is None:
            raise TypeError("model_class è richiesto")
        if not issubclass(model_class, BaseModel):
            raise ValueError("model_class deve essere una sottoclasse di BaseModel")
        self.model_class = model_class

    def index(self) -> Dict[str, Any]:
        """Metodo base per l'index"""
        return {
            'success': True,
            'message': 'Base controller index'
        }

    def health_check(self) -> Dict[str, Any]:
        """Controllo dello stato del controller"""
        return {
            'status': 'healthy',
            'model': self.model_class.__name__
        }

    def handle_error(self, message: str) -> Dict[str, Any]:
        """Gestione degli errori"""
        return {
            'success': False,
            'message': str(message)
        }
