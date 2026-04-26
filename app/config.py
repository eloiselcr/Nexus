import os
from pathlib import Path

# /Users/eloiselcr/Documents/Nexus/app/config.py
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Configuration de base de l'application NexusGraph."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-nexus-local-only-123'
    
    # Chemins relatifs calculés dynamiquement pour garantir la portabilité (Clé USB)
    DATA_DIR = BASE_DIR / 'data'
    DATABASE_URI = DATA_DIR / 'nexusgraph.db'
    
    # Création du dossier data s'il n'existe pas
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Configuration Flask
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    TESTING = False
