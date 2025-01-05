from app.controllers.base import BaseController
from app.services.sheet_service import SheetService

class SheetController(BaseController):
    def __init__(self):
        super().__init__()
    
    def index(self):
        """Lista dei fogli"""
        try:
            sheets = SheetService.get_all_sheets()
            return self.render_view('sheet/index.html', 
                                  sheets=sheets,
                                  title="Fogli")
        except Exception as e:
            return self.handle_error(str(e))
    
    def create(self):
        """Creazione nuovo foglio"""
        try:
            return self.render_view('sheet/create.html',
                                  title="Nuovo Foglio")
        except Exception as e:
            return self.handle_error(str(e))
    
    def view(self, sheet_id):
        """Visualizzazione singolo foglio"""
        try:
            sheet = SheetService.get_sheet(sheet_id)
            return self.render_view('sheet/view.html',
                                  sheet=sheet,
                                  title=f"Foglio - {sheet['name']}")
        except Exception as e:
            return self.handle_error(str(e)) 