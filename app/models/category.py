from peewee import CharField, BooleanField, DateTimeField
import datetime
from app.models.base import BaseModel

# /Users/eloiselcr/Documents/Nexus/app/models/category.py

class Category(BaseModel):
    """Définit les catégories de pages (Personne, Réunion, Projet...).
    Contrôle l'apparence sur le graphe et les templates associés.
    """
    name = CharField(unique=True, max_length=50)
    icon = CharField(max_length=10, default='📄')
    color = CharField(max_length=20, default='#6366f1')
    graph_shape = CharField(max_length=20, default='ellipse')
    is_visible_on_graph = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'categories'
