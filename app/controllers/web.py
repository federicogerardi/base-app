from app.controllers.base import BaseController
from app.services.web_service import WebService

class WebController(BaseController):
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Logica per la pagina principale.
        
        Recupera i dati necessari per la homepage e rende il template.
        """
        try:
            home_data = WebService.get_home_data()
            return self.render_view('index.html',
                                  title="Home",
                                  **home_data)
        except Exception as e:
            return self.handle_error(str(e)) 