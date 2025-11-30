# app/routes/chat_routes.py - VERSIÓN OPTIMIZADA

import logging
from flask import Blueprint, request, jsonify
from functools import lru_cache
import hashlib
from app.rag.chain import create_chain
from app.core.session_manager import session_manager
from app.services.classification_service import ClassificationService
from app.services.response_service import ResponseService

logger = logging.getLogger(__name__)

# Crear blueprint
chat_bp = Blueprint('chat', __name__)

# Inicializar servicios (SINGLETON)
qa_chain = None
llm_model = None
classification_service = None
response_service = None

# Cache simple para respuestas (en producción usar Redis)
response_cache = {}
MAX_CACHE_SIZE = 100

def get_cache_key(query: str) -> str:
    """Genera una clave de cache para una query"""
    return hashlib.md5(query.lower().strip().encode()).hexdigest()

try:
    logger.info("[INIT] Iniciando servicios...")
    qa_chain, llm_model = create_chain()
    classification_service = ClassificationService(llm_model)
    response_service = ResponseService(qa_chain, llm_model)
    logger.info("[INIT] ✅ Servicios inicializados correctamente")
except Exception as e:
    logger.error(f"[INIT] ⚠️ Error al inicializar servicios: {str(e)}")

@chat_bp.route('/ask', methods=['POST'])
def ask_question():
    """Endpoint para realizar consultas sobre el código de tránsito"""
    
    # Verificar que los servicios estén disponibles
    if not all([qa_chain, llm_model, classification_service, response_service]):
        return jsonify({
            "error": "Servicio no disponible. Intente más tarde."
        }), 503

    try:
        # Validar request
        if not request.is_json:
            return jsonify({
                "error": "Se requiere Content-Type: application/json"
            }), 400
        
        data = request.get_json()
        
        # Validar campo query
        if 'query' not in data or not data['query']:
            return jsonify({
                "error": "El campo 'query' es requerido"
            }), 400
        
        query = data['query'].strip()
        
        # OPTIMIZACIÓN 1: Cache de respuestas
        cache_key = get_cache_key(query)
        if cache_key in response_cache:
            logger.info(f"[CACHE HIT] Respuesta en cache para: {query[:50]}")
            cached_response = response_cache[cache_key].copy()
            
            # Actualizar session_id pero mantener respuesta
            session_id = request.headers.get('X-Session-ID')
            session_id = session_manager.get_or_create_session(session_id)
            cached_response['session_id'] = session_id
            
            # Guardar en historial
            session_manager.add_message(
                session_id=session_id,
                user_message=query,
                assistant_message=cached_response['response']
            )
            
            return jsonify(cached_response), 200
        
        # Obtener o crear sesión
        session_id = request.headers.get('X-Session-ID')
        session_id = session_manager.get_or_create_session(session_id)
        
        logger.info(f"[ASK] Session: {session_id[:20]}... | Query: {query[:100]}...")

        # OPTIMIZACIÓN 2: Clasificación simplificada para queries cortas
        if len(query.split()) <= 3:
            # Para queries muy cortas, usar clasificación rápida
            category = "GENERAL"
            intent = 1
        else:
            # Clasificar y analizar consulta
            category, intent = classification_service.analyze_query(query)

        # OPTIMIZACIÓN 3: Obtener historial solo si es necesario
        history = ""
        if len(session_manager.get_messages(session_id)) > 0:
            history = session_manager.get_history(session_id, max_messages=3)  # Reducido de 5 a 3

        # Procesar consulta y generar respuesta
        result = response_service.process_query(
            query=query,
            category=category,
            history=history
        )

        # Guardar en historial
        session_manager.add_message(
            session_id=session_id,
            user_message=query,
            assistant_message=result['response']
        )

        # Construir respuesta
        response = {
            "response": result['response'],
            "sources": result['sources'],
            "context_used": result['context_used'],
            "session_id": session_id,
            "category": category,
            "intent": intent
        }

        # OPTIMIZACIÓN 4: Guardar en cache (con límite de tamaño)
        if len(response_cache) >= MAX_CACHE_SIZE:
            # Eliminar la entrada más antigua (FIFO simple)
            first_key = next(iter(response_cache))
            del response_cache[first_key]
        
        response_cache[cache_key] = {
            "response": result['response'],
            "sources": result['sources'],
            "context_used": result['context_used'],
            "category": category,
            "intent": intent
        }

        logger.info(f"[ASK] Respuesta generada exitosamente para sesión: {session_id[:20]}...")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"❌ Error procesando pregunta: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Ocurrió un error al procesar tu consulta. Por favor intenta nuevamente."
        }), 500

@chat_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """Endpoint para limpiar el historial de conversación"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id') or request.headers.get('X-Session-ID')
        
        if not session_id:
            return jsonify({
                "error": "Se requiere session_id"
            }), 400
        
        success = session_manager.clear_session(session_id)
        
        if success:
            return jsonify({
                "message": "Historial limpiado correctamente",
                "session_id": session_id
            }), 200
        
        return jsonify({
            "error": "Sesión no encontrada"
        }), 404
        
    except Exception as e:
        logger.error(f"Error limpiando historial: {str(e)}")
        return jsonify({
            "error": "Error al limpiar historial"
        }), 500

@chat_bp.route('/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """Endpoint para obtener información de una sesión"""
    try:
        info = session_manager.get_session_info(session_id)
        
        if info:
            return jsonify(info), 200
        
        return jsonify({
            "error": "Sesión no encontrada"
        }), 404
        
    except Exception as e:
        logger.error(f"Error obteniendo información de sesión: {str(e)}")
        return jsonify({
            "error": "Error al obtener información de sesión"
        }), 500

@chat_bp.route('/sessions/active', methods=['GET'])
def get_active_sessions():
    """Endpoint para obtener el número de sesiones activas"""
    try:
        # Limpiar sesiones expiradas primero
        session_manager.cleanup_expired_sessions()
        
        count = session_manager.get_active_sessions_count()
        
        return jsonify({
            "active_sessions": count,
            "cache_size": len(response_cache)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo sesiones activas: {str(e)}")
        return jsonify({
            "error": "Error al obtener sesiones activas"
        }), 500

@chat_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Endpoint para limpiar el cache de respuestas"""
    try:
        global response_cache
        response_cache = {}
        
        return jsonify({
            "message": "Cache limpiado correctamente"
        }), 200
        
    except Exception as e:
        logger.error(f"Error limpiando cache: {str(e)}")
        return jsonify({
            "error": "Error al limpiar cache"
        }), 500