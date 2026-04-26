from flask import Blueprint, jsonify, request
import datetime
from app.models import Page

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Route de test pour vérifier que l'API JSON fonctionne."""
    return jsonify({"status": "ok", "message": "NexusGraph API is running"})

@api_bp.route('/page/<int:page_id>', methods=['PUT'])
def update_page(page_id):
    """Met à jour le contenu et le titre d'une page."""
    page = Page.get_or_none(Page.id == page_id)
    if not page:
        return jsonify({"error": "Page introuvable"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400
        
    if 'title' in data:
        page.title = data['title']
    if 'content' in data:
        page.content = data['content']
        # TODO: Phase 4 - Extraire le raw_text pour la recherche FTS
        # TODO: Phase 4 - Parser les @mentions et générer les liens automatiques
        
    page.updated_at = datetime.datetime.now()
    page.save()
    
    return jsonify({"status": "success", "message": "Page sauvegardée", "updated_at": page.updated_at.isoformat()})
