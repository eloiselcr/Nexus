from flask import Flask, jsonify
from peewee import OperationalError
import logging

from app.config import Config
from app.models.base import db

# /Users/eloiselcr/Documents/Nexus/app/__init__.py

def create_app(config_class=Config) -> Flask:
    """Application Factory: Initialise l'application Flask de manière modulaire.
    
    Args:
        config_class: La classe de configuration à utiliser.
        
    Returns:
        L'instance Flask configurée.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configuration du logger
    if app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG)

    # --- Enregistrement des Blueprints ---
    # Pour l'instant, on crée des blueprints factices inline. 
    # Ils seront déplacés dans le dossier /routes dans la prochaine étape.
    from app.routes.views_bp import views_bp
    from app.routes.api_bp import api_bp
    from app.routes.errors_bp import errors_bp
    
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(errors_bp)

    # --- Hooks Peewee / SQLite ---
    @app.before_request
    def before_request():
        """Ouvre la connexion SQLite avant chaque requête si elle est fermée."""
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def teardown_request(exc):
        """Ferme la connexion SQLite proprement à la fin de la requête.
        Prévient l'erreur 'Database is locked'.
        """
        if not db.is_closed():
            db.close()

    # Custom Jinja Filter for French Dates
    @app.template_filter('format_datetime_fr')
    def format_datetime_fr(value, format='datetime'):
        if not value:
            return ""
            
        import datetime
        if isinstance(value, str):
            try:
                # SQLite fallback parsing
                value = datetime.datetime.strptime(value.split('.')[0], "%Y-%m-%d %H:%M:%S")
            except Exception:
                try:
                    value = datetime.datetime.fromisoformat(value)
                except:
                    return value # return string if parsing fails
                    
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        
        try:
            day_name = days[value.weekday()]
        except AttributeError:
            return str(value)
        month_name = months[value.month - 1]
        
        if format == 'date':
            return f"{value.day} {month_name} {value.year}"
        elif format == 'full':
            return f"{day_name} {value.day} {month_name} {value.year}"
        else: # datetime
            return f"{value.day} {month_name} {value.year} à {value.strftime('%H:%M')}"
            
    return app
