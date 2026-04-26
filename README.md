# NexusGraph

**NexusGraph** est un outil de gestion des connaissances systémique, hors-ligne (Air-gapped) et conçu pour résoudre le problème de fragmentation de l'information. Il remplace les approches linéaires par un modèle basé sur l'axiome "Tout est une Page", relié par un graphe contextuel automatique.

## Architecture

NexusGraph est conçu pour fonctionner sur une machine isolée d'internet (sur réseau d'entreprise restreint) sous Windows.

- **Backend** : Python 3.12, Flask.
- **Base de données** : SQLite 3 (via l'ORM Peewee).
- **Frontend** : HTML5, CSS3 natif, Jinja2 (Templates).
- **Éditeur Riche** : Quill.js (v2).
- **Moteur de Graphe** : Cytoscape.js.

## Lancement

Aucune installation `pip` n'est requise sur la machine cible. Les dépendances sont "vendorées" (embarquées localement).

1. Double-cliquez sur `launch.py` ou exécutez `python launch.py`.
2. Ouvrez un navigateur (Firefox/Chrome) sur `http://127.0.0.1:8080`.

## Principes Fondamentaux

1. **Le Flux (Espaces)** : Espaces de travail cloisonnés pour les projets en cours (Silos stricts).
2. **Le Stock (Global)** : Référentiel de l'entreprise (Personnes, SI, Savoirs transverses).
3. **La Lampe Torche** : Le graphe montre toujours le voisinage direct de la note courante, évitant l'effet "plat de spaghettis" illisible.
4. **Mentions Intégrées** : Tapez `@nom` dans l'éditeur pour lier automatiquement deux pages.

## Installation et Lancement (Tutoriel)

NexusGraph est conçu pour être portable ("Air-gapped"). Aucune connexion internet n'est requise lors du lancement, toutes les dépendances (Python et JavaScript) sont embarquées.

### Pré-requis
- **Python 3.12** installé sur la machine cible.
- Un navigateur web moderne (Firefox, Chrome, Edge).

### Lancement
1. Téléchargez ou copiez le dossier `NexusGraph` sur votre clé USB ou machine locale.
2. Ouvrez un terminal (ou l'invite de commande Windows).
3. Naviguez vers le dossier du projet : `cd /chemin/vers/NexusGraph`
4. Lancez le script de démarrage : `python launch.py`
5. Ouvrez votre navigateur et allez sur **`http://127.0.0.1:8080`**.

## Architecture des fichiers

- `launch.py` : Point d'entrée de l'application. Lance le serveur Flask.
- `seed.py` : Script d'initialisation de la base de données avec des fausses données.
- `nexusgraph.db` : Base de données SQLite locale (générée automatiquement).
- **`app/`** : Cœur de l'application Flask
  - `__init__.py` : Factory Flask et filtres Jinja.
  - **`models/`** : Les modèles de données Peewee (`page.py`, `space.py`, etc.).
  - **`routes/`** : Les contrôleurs (`views_bp.py` pour le HTML, `api_bp.py` pour le JSON).
  - **`templates/`** : Les vues HTML propulsées par Jinja2 (`base.html`, `page.html`, etc.).
  - **`static/`** : Les assets statiques (CSS, Fonts, JS de Quill et Cytoscape).
- **`vendor/`** : Les librairies Python pré-compilées (Flask, Peewee) pour le mode hors-ligne.
- **`docs/`** : Spécifications fonctionnelles et techniques.
