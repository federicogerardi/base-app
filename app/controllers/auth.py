from flask import redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app.controllers.base import BaseController
from app.models.user import User
from app.core.database import db
from app.forms.auth_forms import LoginForm, RegistrationForm
from app.services.auth_service import AuthService

class AuthController(BaseController):
    def __init__(self):
        super().__init__(model_class=User)
    
    def login(self):
        """Gestisce la pagina di login"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
            
        form = LoginForm()
        return self.render_view('auth/login.html', 
                              title="Accedi",
                              form=form)
    
    def login_post(self):
        """Gestisce il processo di login"""
        try:
            form = LoginForm()
            current_app.logger.info(f"Login attempt with email: {form.email.data}")
            
            if form.validate_on_submit():
                current_app.logger.info("Form validated")
                success, message, user = AuthService.login(
                    email=form.email.data,
                    password=form.password.data
                )
                
                if success:
                    login_user(user, remember=form.remember_me.data)
                    next_page = request.args.get('next')
                    if not next_page or not next_page.startswith('/'):
                        next_page = url_for('dashboard.index')
                    
                    flash('Login effettuato con successo!', 'success')
                    return redirect(next_page)
                else:
                    current_app.logger.warning(f"Failed login attempt for email: {form.email.data}")
                    flash(message, 'danger')
            else:
                current_app.logger.warning("Form validation failed")
                flash('Email o password non validi', 'danger')
                
            return redirect(url_for('auth.login'))
        except Exception as e:
            current_app.logger.error(f"Login error: {str(e)}")
            return self.handle_error(str(e))

    def register(self):
        """Gestisce la pagina di registrazione"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
            
        form = RegistrationForm()
        return self.render_view('auth/register.html', 
                              title="Registrati",
                              form=form)
    
    def register_post(self):
        """Gestisce il processo di registrazione"""
        try:
            form = RegistrationForm()
            
            if form.validate_on_submit():
                success, message, user = AuthService.register_user(
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                )
                
                if success:
                    flash('Registrazione completata con successo!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash(message, 'danger')
                    return redirect(url_for('auth.register'))
                
            return self.render_view('auth/register.html', 
                                  title="Registrati",
                                  form=form)
        except Exception as e:
            return self.handle_error(str(e))

    def logout(self):
        """Gestisce il processo di logout"""
        try:
            success, message = AuthService.logout()
            if success:
                flash(message, 'success')
            else:
                flash(message, 'danger')
            return redirect(url_for('auth.login'))
        except Exception as e:
            return self.handle_error(str(e)) 