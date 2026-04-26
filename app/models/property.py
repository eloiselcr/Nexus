from peewee import CharField, TextField, ForeignKeyField
from app.models.base import BaseModel
from app.models.page import Page

# /Users/eloiselcr/Documents/Nexus/app/models/property.py

class Property(BaseModel):
    """Stocke les métadonnées structurées d'une page (ex: Téléphone: 06...).
    Format Clé-Valeur lié à une Page spécifique.
    """
    page = ForeignKeyField(Page, backref='properties', on_delete='CASCADE')
    key = CharField(max_length=100)
    value = TextField(null=True)

    class Meta:
        table_name = 'properties'
        indexes = (
            (('page', 'key'), True), # Une seule valeur par clé pour une page donnée
        )
