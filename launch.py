import sys
import os
from pathlib import Path

# /Users/eloiselcr/Documents/Nexus/launch.py

# 1. --- VENDORING MAGIC ---
# On récupère le chemin absolu du dossier courant
BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / 'vendor'

# On crée le dossier vendor s'il n'existe pas (utile pour le premier lancement)
os.makedirs(VENDOR_DIR, exist_ok=True)

# On injecte le dossier /vendor EN PREMIER dans le sys.path.
# Ainsi, Python chargera les modules (Flask, Peewee) depuis ce dossier local
# avant de chercher dans l'installation système. C'est la clé du fonctionnement offline.
sys.path.insert(0, str(VENDOR_DIR))

# 2. --- LANCEMENT DE L'APP ---
# Maintenant que le path est modifié, on peut importer Flask et notre app
try:
    from app import create_app
except ImportError as e:
    print("❌ ERREUR CRITIQUE : Impossible d'importer Flask ou l'application.")
    print(f"Détail : {e}")
    print("\nAvez-vous bien exécuté le script de préparation (prepare.sh) sur un poste connecté ?")
    print(f"Le dossier attendu pour les dépendances est : {VENDOR_DIR}")
    sys.exit(1)

# Initialisation
app = create_app()

if __name__ == '__main__':
    print("🚀 Démarrage de NexusGraph en mode local...")
    print("Accès navigateur : http://127.0.0.1:8080")
    
    # Lancement du serveur de développement Flask
    # On écoute sur le port 8080 pour éviter le conflit avec AirPlay sur Mac (port 5000 -> 403 Forbidden)
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)
