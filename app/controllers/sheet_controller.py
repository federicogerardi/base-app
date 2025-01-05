from flask import render_template
from app.services.sheet_service import SheetService

class SheetController:
    @staticmethod
    def index():
        """Lista dei fogli demo"""
        sheets = SheetService.get_all_sheets()
        return render_template('sheet/index.html', 
                            sheets=sheets,
                            title="Fogli")
    
    @staticmethod
    def create():
        """Form di creazione nuovo foglio (demo)"""
        return render_template('sheet/create.html',
                            title="Nuovo Foglio")
    
    @staticmethod
    def view(sheet_id):
        """Visualizzazione foglio demo"""
        sheet = SheetService.get_sheet(sheet_id)
        return render_template('sheet/view.html',
                            sheet=sheet,
                            title=f"Foglio - {sheet['name']}") 