from peewee import CharField, TextField, DateTimeField, IntegerField
import datetime
from app.models.base import BaseModel

# /Users/eloiselcr/Documents/Nexus/app/models/space.py

class Space(BaseModel):
    """Représente un Espace SI ou un contexte de travail.
    Permet de regrouper les pages opérationnelles.
    """
    name = CharField(unique=True, max_length=100)
    description = TextField(null=True)
    color = CharField(max_length=20, default='#10b981')
    order_index = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(null=True)

    class Meta:
        table_name = 'spaces'
