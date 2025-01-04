from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.route('/')
def index():
    """Homepage dell'applicazione web"""
    return render_template('index.html')

@web.route('/about')
def about():
    """Pagina About"""
    return render_template('about.html')

@web.route('/dashboard')
def dashboard():
    """Dashboard dell'applicazione"""
    return render_template('dashboard.html') 