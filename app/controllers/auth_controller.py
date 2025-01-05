from flask import redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.controllers.base import BaseController
from app.models.user import User
from app.core.database import db
from app.forms.auth_forms import LoginForm, RegistrationForm

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
            
            if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                
                if user and user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    user.update_last_login()
                    
                    next_page = request.args.get('next')
                    if not next_page or not next_page.startswith('/'):
                        next_page = url_for('dashboard.index')
                        
                    flash('Login effettuato con successo!', 'success')
                    return redirect(next_page)
                
            flash('Email o password non validi', 'danger')
            return redirect(url_for('auth.login'))
        except Exception as e:
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
                if User.query.filter_by(email=form.email.data).first():
                    flash('Email già registrata', 'danger')
                    return redirect(url_for('auth.register'))
                    
                if User.query.filter_by(username=form.username.data).first():
                    flash('Username già in uso', 'danger')
                    return redirect(url_for('auth.register'))
                
                user = User(
                    email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                )
                
                db.session.add(user)
                db.session.commit()
                
                flash('Registrazione completata con successo!', 'success')
                return redirect(url_for('auth.login'))
                
            return self.render_view('auth/register.html', 
                                  title="Registrati",
                                  form=form)
        except Exception as e:
            return self.handle_error(str(e))

    def logout(self):
        """Gestisce il processo di logout"""
        try:
            logout_user()
            flash('Logout effettuato con successo!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            return self.handle_error(str(e)) 