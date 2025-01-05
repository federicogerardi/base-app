import pytest
from app.forms.auth_forms import LoginForm, RegistrationForm

def test_login_form_validation(app):
    """Test validazione LoginForm"""
    with app.test_request_context():
        # Test form valido
        form = LoginForm(
            email='test@example.com',
            password='password123'
        )
        assert form.validate() is True

        # Test email invalida
        form = LoginForm(
            email='not-an-email',
            password='password123'
        )
        assert form.validate() is False
        assert 'email valida' in str(form.email.errors).lower()

        # Test campi vuoti
        form = LoginForm(
            email='',
            password=''
        )
        assert form.validate() is False
        assert form.email.errors
        assert form.password.errors

def test_registration_form_validation(app):
    """Test validazione RegistrationForm"""
    with app.test_request_context():
        # Test form valido
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is True

        # Test password non corrispondenti
        form = RegistrationForm(
            username='testuser',
            email='test@example.com',
            password='password123',
            confirm_password='different'
        )
        assert form.validate() is False
        assert 'password devono coincidere' in str(form.confirm_password.errors).lower()

        # Test username troppo corto
        form = RegistrationForm(
            username='te',
            email='test@example.com',
            password='password123',
            confirm_password='password123'
        )
        assert form.validate() is False
        assert 'caratteri' in str(form.username.errors).lower() 