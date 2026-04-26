from peewee import CharField, ForeignKeyField, DateTimeField
import datetime
from app.models.base import BaseModel
from app.models.page import Page

# /Users/eloiselcr/Documents/Nexus/app/models/link.py

class Link(BaseModel):
    """Représente une relation orientée entre deux pages.
    Peut être une relation structurelle forte (propriété) ou faible (mention).
    """
    source = ForeignKeyField(Page, backref='outgoing_links', on_delete='CASCADE')
    target = ForeignKeyField(Page, backref='incoming_links', on_delete='CASCADE')
    
    # Type de lien: 'structural' ou 'mention'
    link_type = CharField(max_length=20, default='mention')
    
    # Label affiché sur l'arête du graphe (ex: "appartient à", "mentionne")
    label = CharField(max_length=50, null=True)
    
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'links'
        indexes = (
            # Contrainte d'unicité pour ne pas dupliquer les mêmes liens
            (('source', 'target', 'link_type'), True),
        )
