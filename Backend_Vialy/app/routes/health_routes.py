"""
Rutas de salud y estado del servicio.
"""

import logging
from flask import Blueprint, jsonify
from app.config.settings import Config
from app.core.session_manager import session_manager

logger = logging.getLogger(__name__)

# Crear blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    from app.routes.chat_routes import qa_chain, llm_model
    
    # Limpiar sesiones expiradas
    session_manager.cleanup_expired_sessions()
    
    return jsonify({
        "status": "healthy" if qa_chain and llm_model else "degraded",
        "model": Config.MODEL_NAME,
        "ready": qa_chain is not None,
        "active_sessions": session_manager.get_active_sessions_count(),
        "version": Config.API_VERSION
    }), 200

@health_bp.route('/', methods=['GET'])
def root():
    """Endpoint raíz con información de la API"""
    return jsonify({
        "message": Config.API_TITLE + " 🇨🇴",
        "endpoints": {
            "documentación": "/docs",
            "salud": "/health",
            "consultas": "/ask (POST)",
            "limpiar_historial": "/clear-history (POST)",
            "info_sesión": "/session/<session_id> (GET)",
            "sesiones_activas": "/sessions/active (GET)"
        },
        "version": Config.API_VERSION,
        "features": [
            "Contexto conversacional",
            "Clasificación automática de consultas",
            "Múltiples prompts especializados",
            "RAG con Gemini",
            "Gestión de sesiones"
        ]
    }), 200

@health_bp.route('/ping', methods=['GET'])
def ping():
    """Endpoint simple para verificar conectividad"""
    return jsonify({"status": "pong"}), 200