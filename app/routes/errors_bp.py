from flask import Blueprint, jsonify

# /Users/eloiselcr/Documents/Nexus/app/routes/errors_bp.py

errors_bp = Blueprint('errors', __name__)

@errors_bp.app_errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Resource not found", "code": 404}), 404

@errors_bp.app_errorhandler(500)
def handle_500(e):
    return jsonify({"error": "Internal server error", "code": 500}), 500
