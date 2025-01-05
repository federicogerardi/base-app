"""
Modulo degli helper per i template.

Fornisce funzioni helper per i template Jinja, come `safe_url_for`, che
gestisce in modo sicuro la generazione degli URL per gli endpoint.
"""

from flask import url_for, current_app
from datetime import datetime

def safe_url_for(endpoint, **kwargs):
    """
    Genera un URL sicuro per un endpoint.
    Ritorna '#' se l'endpoint non esiste.
    """
    try:
        # Verifica che l'endpoint esista prima di chiamare url_for
        if endpoint in current_app.view_functions:
            return url_for(endpoint, **kwargs)
        current_app.logger.warning(f"Tentativo di accesso a endpoint inesistente: {endpoint}")
        return "#"
    except Exception as e:
        current_app.logger.warning(f"Errore nella generazione URL per {endpoint}: {str(e)}")
        return "#"

def format_datetime(value):
    """
    Formatta una data in formato leggibile.
    Se la data è una stringa, prova a convertirla in datetime.
    """
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    return value.strftime('%d/%m/%Y')

def init_template_helpers(app):
    """Inizializza gli helper per i template."""
    app.jinja_env.globals.update(safe_url_for=safe_url_for)
    # Registra il filtro datetime
    app.jinja_env.filters['datetime'] = format_datetime 