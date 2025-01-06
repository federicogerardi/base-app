from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from app.models.user import UserRole

def admin_required(f):
    """Decoratore per richiedere permessi di amministratore."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            flash('Accesso negato. Solo gli amministratori possono accedere a questa sezione.', 'danger')
            return redirect(url_for('web.index'))  # Reindirizza a una pagina appropriata
        return f(*args, **kwargs)
    return decorated_function 