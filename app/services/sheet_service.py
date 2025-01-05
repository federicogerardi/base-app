class SheetService:
    @staticmethod
    def get_all_sheets():
        """Restituisce una lista di fogli demo"""
        return [
            {
                'id': 1,
                'name': 'Foglio Demo 1',
                'description': 'Questo è un foglio di esempio',
                'created_at': '2024-01-15',
                'status': 'active',
                'status_color': 'success'
            },
            {
                'id': 2,
                'name': 'Foglio Demo 2',
                'description': 'Un altro foglio di esempio',
                'created_at': '2024-01-16',
                'status': 'draft',
                'status_color': 'secondary'
            }
        ]
    
    @staticmethod
    def get_sheet(sheet_id):
        """Restituisce un foglio demo specifico"""
        return {
            'id': sheet_id,
            'name': f'Foglio Demo {sheet_id}',
            'description': 'Questo è un foglio di esempio',
            'created_at': '2024-01-15',
            'status': 'active',
            'status_color': 'success'
        } 