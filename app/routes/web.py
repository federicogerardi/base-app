from flask import Blueprint, render_template

web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/about')
def about():
    return render_template('about.html')

# Rimuovi o commenta la vecchia route dashboard se presente