import sqlite3
from peewee import SqliteDatabase, Model
from app.config import Config

# /Users/eloiselcr/Documents/Nexus/app/models/base.py

# Initialisation de la base de données Peewee
# On utilise les pragmas pour optimiser SQLite (performances et intégrité)
db = SqliteDatabase(
    Config.DATABASE_URI,
    pragmas={
        'journal_mode': 'wal',  # Write-Ahead Logging pour la concurrence
        'cache_size': -1024 * 64,  # 64MB cache
        'foreign_keys': 1,      # Activer les clés étrangères
        'ignore_check_constraints': 0,
        'synchronous': 0
    }
)

class BaseModel(Model):
    """Classe de base pour tous les modèles Peewee.
    Lie automatiquement les modèles à la base de données SQLite.
    """
    class Meta:
        database = db
