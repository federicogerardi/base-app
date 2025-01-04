from flask import url_for, current_app

def safe_url_for(endpoint, **kwargs):
    """
    Wrapper sicuro per url_for che gestisce endpoints inesistenti
    Ritorna # se l'endpoint non esiste
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

def init_template_helpers(app):
    """Inizializza gli helper per i template"""
    app.jinja_env.globals.update(safe_url_for=safe_url_for) 