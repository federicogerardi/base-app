from flask import Blueprint, render_template
from app.core.auth import auth_required

web = Blueprint('web', __name__, template_folder='../templates')

@web.route('/')
def index():
    """Homepage dell'applicazione web"""
    return render_template('index.html')

@web.route('/about')
def about():
    """Pagina About"""
    return render_template('about.html')

# Route dashboard temporaneamente disattivata
# @web.route('/dashboard')
# @auth_required
# def dashboard():
#     """Dashboard dell'applicazione (richiede autenticazione)"""
#     return render_template('dashboard.html') 