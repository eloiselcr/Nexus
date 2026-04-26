# /Users/eloiselcr/Documents/Nexus/app/models/__init__.py
from app.models.base import db, BaseModel
from app.models.category import Category
from app.models.space import Space
from app.models.page import Page
from app.models.link import Link
from app.models.property import Property

# Liste de tous les modèles pour la création automatique des tables
MODELS = [Category, Space, Page, Link, Property]

def init_db():
    """Crée les tables SQLite si elles n'existent pas."""
    db.connect(reuse_if_open=True)
    db.create_tables(MODELS)
    db.close()
