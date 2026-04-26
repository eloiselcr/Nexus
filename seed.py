import sys
from pathlib import Path

# /Users/eloiselcr/Documents/Nexus/seed.py

# Vendoring magic (pour pouvoir lancer ce script en standalone)
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'vendor'))

from app.models import init_db, Category, Space

def seed_database():
    """Initialise la base de données avec les catégories par défaut."""
    print("⏳ Initialisation de la base de données SQLite...")
    init_db()
    print("✅ Tables créées avec succès.")

    print("⏳ Création des catégories par défaut...")
    categories = [
        {'name': 'Personne', 'icon': '👤', 'color': '#8b5cf6', 'graph_shape': 'ellipse', 'is_visible_on_graph': True},
        {'name': 'Organisation', 'icon': '🏢', 'color': '#f59e0b', 'graph_shape': 'round-rectangle', 'is_visible_on_graph': True},
        {'name': 'Projet', 'icon': '📊', 'color': '#10b981', 'graph_shape': 'hexagon', 'is_visible_on_graph': True},
        {'name': 'Savoir', 'icon': '📚', 'color': '#ec4899', 'graph_shape': 'diamond', 'is_visible_on_graph': True},
        {'name': 'Réunion', 'icon': '📋', 'color': '#3b82f6', 'graph_shape': 'round-tag', 'is_visible_on_graph': False},
        {'name': 'Note technique', 'icon': '📄', 'color': '#64748b', 'graph_shape': 'round-tag', 'is_visible_on_graph': False},
        {'name': 'Point de suivi', 'icon': '📌', 'color': '#ef4444', 'graph_shape': 'round-tag', 'is_visible_on_graph': False},
        {'name': 'Note libre', 'icon': '📝', 'color': '#9ca3af', 'graph_shape': 'round-tag', 'is_visible_on_graph': False},
    ]

    for cat_data in categories:
        cat, created = Category.get_or_create(name=cat_data['name'], defaults=cat_data)
        if created:
            print(f"  + Catégorie ajoutée : {cat.name}")
        else:
            print(f"  = Catégorie existante : {cat.name}")

    print("⏳ Création de l'Espace 'Global' par défaut...")
    space, created = Space.get_or_create(name='Global', defaults={'description': 'Espace référentiel transverse', 'color': '#6366f1'})
    if created:
        print("  + Espace 'Global' créé.")
    else:
        print("  = Espace 'Global' existant.")

    print("🎉 Seeding terminé !")

if __name__ == '__main__':
    seed_database()
