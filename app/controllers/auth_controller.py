from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.core.database import db
from app.forms.auth_forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash

class AuthController:
    @staticmethod
    def login():
        """Gestisce la pagina di login"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
            
        form = LoginForm()
        return render_template('auth/login.html', 
                             title="Accedi",
                             form=form)
    
    @staticmethod
    def login_post():
        """Gestisce il processo di login"""
        form = LoginForm()
        
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                user.update_last_login()
                
                # Redirect alla pagina richiesta originariamente (se presente)
                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('dashboard.index')
                    
                flash('Login effettuato con successo!', 'success')
                return redirect(next_page)
            
        flash('Email o password non validi', 'danger')
        return redirect(url_for('auth.login'))

    @staticmethod
    def register():
        """Gestisce la pagina di registrazione"""
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
            
        form = RegistrationForm()
        return render_template('auth/register.html', 
                             title="Registrati",
                             form=form)
    
    @staticmethod
    def register_post():
        """Gestisce il processo di registrazione"""
        form = RegistrationForm()
        
        if form.validate_on_submit():
            # Verifica se l'email o l'username esistono già
            if User.query.filter_by(email=form.email.data).first():
                flash('Email già registrata', 'danger')
                return redirect(url_for('auth.register'))
                
            if User.query.filter_by(username=form.username.data).first():
                flash('Username già in uso', 'danger')
                return redirect(url_for('auth.register'))
            
            # Crea il nuovo utente
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=form.password.data  # La password viene criptata automaticamente
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registrazione completata con successo! Ora puoi effettuare il login.', 'success')
            return redirect(url_for('auth.login'))
            
        return render_template('auth/register.html', 
                             title="Registrati",
                             form=form)

    @staticmethod
    def logout():
        """Gestisce il processo di logout"""
        logout_user()
        flash('Logout effettuato con successo!', 'success')
        return redirect(url_for('auth.login')) 