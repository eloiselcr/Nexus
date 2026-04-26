import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from playhouse.migrate import migrate, SqliteMigrator
from peewee import IntegerField, DateTimeField
from app.models.base import db
from app.models.space import Space

def run_migration():
    migrator = SqliteMigrator(db)
    
    order_index_field = IntegerField(default=0)
    deleted_at_field = DateTimeField(null=True)
    
    try:
        migrate(
            migrator.add_column('spaces', 'order_index', order_index_field),
            migrator.add_column('spaces', 'deleted_at', deleted_at_field),
            migrator.add_column('pages', 'deleted_at', deleted_at_field)
        )
        print("Migration réussie: order_index et deleted_at ajoutés.")
        
        # Initialiser l'order_index séquentiellement pour les espaces existants
        spaces = Space.select().order_by(Space.name)
        for i, space in enumerate(spaces):
            space.order_index = i
            space.save()
            
    except Exception as e:
        print(f"Erreur ou migration déjà effectuée : {e}")

if __name__ == '__main__':
    run_migration()
