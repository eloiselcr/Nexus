from peewee import CharField, TextField, DateTimeField, ForeignKeyField
import datetime
from app.models.base import BaseModel
from app.models.category import Category
from app.models.space import Space

# /Users/eloiselcr/Documents/Nexus/app/models/page.py

class Page(BaseModel):
    """L'entité centrale de NexusGraph.
    Représente aussi bien une personne, qu'une réunion ou un projet.
    """
    title = CharField(max_length=255)
    content = TextField(null=True)  # Contenu HTML de Quill
    raw_text = TextField(null=True) # Texte brut pour la recherche FTS
    
    # Relations
    category = ForeignKeyField(Category, backref='pages', on_delete='RESTRICT')
    space = ForeignKeyField(Space, backref='pages', null=True, on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'pages'
