from app import create_app
from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Usa FLASK_DEBUG per determinare l'ambiente
debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
app = create_app('development' if debug_mode else 'production')

if __name__ == '__main__':
    app.run(debug=debug_mode)
