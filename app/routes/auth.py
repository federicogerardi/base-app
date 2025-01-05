from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms.auth_forms import LoginForm, RegistrationForm
from app.services.auth_service import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        success, message, user = AuthService.login(
            email=form.email.data,
            password=form.password.data
        )
        
        if success:
            next_page = request.args.get('next')
            return redirect(next_page or url_for('web.index'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/login.html', form=form, title='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        success, message, user = AuthService.register_user(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        
        if success:
            flash('Registrazione completata con successo! Ora puoi effettuare il login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'danger')
    
    return render_template('auth/register.html', form=form, title='Registrazione')

@bp.route('/logout')
@login_required
def logout():
    success, message = AuthService.logout()
    if success:
        flash('Logout effettuato con successo.', 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('web.index')) 