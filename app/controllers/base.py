from flask import jsonify, render_template
from app.core.exceptions import AppException

class BaseController:
    def __init__(self, model_class=None):
        """
        Inizializza il controller base.
        Args:
            model_class: La classe del modello associato al controller
        """
        self.model_class = model_class
    
    def json_response(self, data, status=200):
        """
        Standardizza le risposte JSON dell'API.
        Args:
            data: Dati da restituire
            status: Status code HTTP (default: 200)
        """
        return jsonify({
            'success': 200 <= status < 300,
            'data': data
        }), status
    
    def render_view(self, template, **kwargs):
        """
        Standardizza il rendering delle viste.
        Args:
            template: Path del template
            kwargs: Variabili da passare al template
        """
        return render_template(template, **kwargs)
    
    def handle_error(self, error, status_code=400):
        """
        Gestisce gli errori in modo uniforme.
        Args:
            error: Messaggio di errore
            status_code: Status code HTTP (default: 400)
        """
        raise AppException(str(error), status_code=status_code)
