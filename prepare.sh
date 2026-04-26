#!/bin/bash

# /Users/eloiselcr/Documents/Nexus/prepare.sh
# Script de préparation pour environnement hors-ligne (Air-gapped)
# À exécuter sur une machine CONNECTÉE À INTERNET (Mac ou PC)

echo "🚀 Démarrage du script de vendoring NexusGraph..."

# 1. Création des dossiers
echo "📂 Création des répertoires..."
mkdir -p vendor
mkdir -p app/static/js
mkdir -p app/static/css
mkdir -p app/static/fonts

# 2. Téléchargement des dépendances Python (Wheels) pour Windows
echo "🐍 Téléchargement des packages Python (ciblage Windows Python 3.12)..."
# On force le téléchargement des versions compilées pour Windows 64 bits
pip download \
  --only-binary=:all: \
  --platform win_amd64 \
  --python-version 3.12 \
  --implementation cp \
  --abi cp312 \
  flask peewee \
  -d vendor/

# 3. Téléchargement des assets Frontend
echo "🌐 Téléchargement des assets Frontend..."

# Cytoscape.js (Graphe)
echo "  -> Cytoscape.js"
curl -sS -o app/static/js/cytoscape.min.js https://unpkg.com/cytoscape@3.30.4/dist/cytoscape.min.js

# Quill.js (Éditeur de texte)
echo "  -> Quill.js"
curl -sS -o app/static/js/quill.min.js https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.js
curl -sS -o app/static/css/quill.snow.css https://cdn.jsdelivr.net/npm/quill@2.0.3/dist/quill.snow.css

# 4. Polices (Inter)
echo "🔤 Téléchargement de la police Inter..."
# Pour simplifier, on télécharge un fichier CSS unifié qui référence les WOFF2.
# Dans une vraie passe de prod stricte, il faudrait télécharger les .woff2 et réécrire le CSS.
# Pour la v0.1, on va simuler la police en CSS local.
cat << 'EOF' > app/static/css/fonts.css
/* Fallback system fonts for complete offline mode if Inter is missing */
:root {
  --font: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
EOF

echo "✅ Terminé !"
echo "Vous pouvez maintenant copier le dossier NexusGraph complet sur la clé USB."
