from app.controllers.base import BaseController

class WebController(BaseController):
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Logica per la pagina principale"""
        try:
            return self.render_view('index.html', 
                                  title="Home")
        except Exception as e:
            return self.handle_error(str(e)) 