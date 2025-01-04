from loguru import logger
import sys
from pathlib import Path

def setup_logger(app):
    # Crea la directory dei log se non esiste
    log_dir = Path(app.root_path).parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Rimuovi tutti i gestori esistenti
    logger.remove()
    
    # Configura il logger per stdout (console)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        level="DEBUG" if app.debug else "INFO"
    )
    
    # Configura il logger per il file
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        rotation="1 day",
        retention="1 month",
        level="INFO"
    )

    return logger