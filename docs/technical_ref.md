# Technical Reference

Ce document référence l'architecture technique de NexusGraph.

## Stack Technologique
- **Python 3.12** : Langage principal.
- **Flask (Factory Pattern)** : Serveur web. Le pattern factory (`create_app`) garantit une configuration propre.
- **Peewee ORM** : Gestion de la base de données SQLite. Choisi pour sa légèreté et sa robustesse en mode single-file.
- **SQLite 3** : Base de données locale (Fichier `nexusgraph.db`).
- **Quill.js** : Éditeur WYSIWYG pour le texte enrichi.
- **Cytoscape.js** : Librairie de rendu de graphe dirigé orienté mathématiques.

## Mode "Air-gapped" (Vendoring)
Le script `launch.py` redéfinit le `sys.path` pour injecter le dossier `/vendor`.
Ce dossier contient les fichiers `.whl` (wheels) de Flask, Peewee et leurs dépendances, pré-compilés pour Windows 64-bits.
Les assets Front-End (CSS, JS, Fonts) sont stockés dans `app/static/`.

## Modèle de Données (Peewee)
- **Space** : Conteneur de travail (Silo). S'il est nul, la page est "Globale".
- **Category** : Définit l'icône, le comportement, et à terme, le template de propriétés d'une page.
- **Page** : L'entité fondamentale. Contient un titre, un contenu HTML, et des liens.
- **Property** : Métadonnées clés-valeurs associées à une page (Typé JSON ou EAV).
- **Link** : Relation orientée (Source $\rightarrow$ Target) représentant les `@mentions` ou l'appartenance structurelle.

## Organisation du Code
- `/app/__init__.py` : Factory Flask et Filtres Jinja personnalisés (ex: dates en français).
- `/app/models/` : Classes Peewee. Hooks `@app.teardown_request` pour gérer les connexions SQLite proprement.
- `/app/routes/` : Blueprints Flask.
  - `views_bp` : Rendu des templates HTML.
  - `api_bp` : Endpoints REST JSON (pour sauvegarde asynchrone et graphe).
  - `errors_bp` : Gestion propre des erreurs 404/500.
- `/app/templates/` : Fichiers Jinja2 (`base.html`, `dashboard.html`, `page.html`).
