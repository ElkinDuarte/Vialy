"""
Rutas de chat - Versión completa con usuario_id y DB
"""

import logging
import hashlib
from flask import Blueprint, request, jsonify, g
from app.config.database import get_db
from app.core.session_manager import SessionManager
from app.models.models import Message  # Importar Message para los endpoints

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

# Servicios globales
qa_chain = None
llm_model = None
classification_service = None
response_service = None
# Cache de respuestas
response_cache = {}
MAX_CACHE_SIZE = 100

def get_cache_key(query: str) -> str:
    """Genera una clave de cache para una query"""
    return hashlib.md5(query.lower().strip().encode()).hexdigest()

def initialize_services():
    """Inicializa todos los servicios necesarios"""
    global qa_chain, llm_model, classification_service, response_service
    
    try:
        logger.info("[INIT] 🚀 Iniciando servicios...")
        
        # 1. Cadena RAG y LLM
        from app.rag.chain import create_chain
        qa_chain, llm_model = create_chain()
        logger.info("[INIT] ✅ Cadena RAG y LLM creados")
        
        # 2. Servicios internos
        from app.services.classification_service import ClassificationService
        from app.services.response_service import ResponseService
        
        classification_service = ClassificationService(llm_model)
        response_service = ResponseService(qa_chain, llm_model)
        logger.info("[INIT] ✅ Servicios de clasificación y respuesta inicializados")
        
        return True
    except Exception as e:
        logger.error(f"[INIT] ❌ Error al inicializar servicios: {str(e)}", exc_info=True)
        return False

services_initialized = initialize_services()

@chat_bp.before_request
def inject_db():
    """Asigna la sesión de DB a g.db para cada request"""
    g.db = next(get_db())

@chat_bp.route('/ask', methods=['POST'])
def ask_question():
    if not services_initialized or not all([qa_chain, llm_model, classification_service, response_service]):
        return jsonify({"error": "Servicios no disponibles", "status": "degraded"}), 503

    try:
        if not request.is_json:
            return jsonify({"error": "Se requiere Content-Type: application/json"}), 400
        
        data = request.get_json()
        query = data.get("query", "").strip()
        if not query or len(query) < 3:
            return jsonify({"error": "Consulta demasiado corta"}), 400

        # Obtener usuario obligatorio
        usuario_id = request.headers.get("X-User-ID")
        if not usuario_id:
            return jsonify({"error": "Se requiere X-User-ID en headers"}), 400
        try:
            usuario_id = int(usuario_id)
        except ValueError:
            return jsonify({"error": "X-User-ID debe ser un entero"}), 400

        # Crear instancia de SessionManager con la conexión a DB
        session_manager = SessionManager(db=g.db)
        
        # Obtener o crear sesión
        session_id = request.headers.get("X-Session-ID")
        session_id = session_manager.get_or_create_session(usuario_id=usuario_id, session_id=session_id)

        # Revisar cache
        cache_key = get_cache_key(query)
        if cache_key in response_cache:
            cached_response = response_cache[cache_key].copy()
            cached_response['session_id'] = session_id
            session_manager.add_message(session_id=session_id, user_message=query, assistant_message=cached_response['response'], category=cached_response.get('category'))
            return jsonify(cached_response), 200

        # Clasificación
        try:
            category, intent = classification_service.analyze_query(query)
        except Exception:
            category = "GENERAL"
            intent = 1

        # 🔴 FALTA ESTA LÍNEA: Obtener historial ANTES de usarlo
        history = session_manager.get_history(session_id, max_messages=3)

        # Generar respuesta
        try:
            if hasattr(response_service, 'process_query'):
                # ✅ Ahora history está definido
                result = response_service.process_query(query=query, category=category, history=history)
            else:
                rag_result = qa_chain.invoke({"query": query})
                source_docs = rag_result.get("source_documents", [])
                context_texts = [doc.page_content.strip() for doc in source_docs]
                context = "\n\n".join(f"- {ctx}" for ctx in context_texts) if context_texts else "Sin contexto."
                # ✅ Ahora history está definido
                response_text = response_service.generate_response(query=query, category=category, history=history, context=context)
                formatted_sources = [
                    {"extracto": doc.page_content[:300], "pagina": doc.metadata.get("page"), "archivo": doc.metadata.get("source", "documento")}
                    for doc in source_docs[:3]
                ]
                result = {"response": response_text, "sources": formatted_sources, "context_used": len(formatted_sources) > 0}
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}", exc_info=True)
            return jsonify({"error": "Error generando respuesta"}), 500

        # Guardar mensajes
        session_manager.add_message(session_id=session_id, user_message=query, assistant_message=result['response'], category=category)

        # Obtener el conversation_id numérico para devolverlo al frontend
        from app.models.models import Conversation
        conv = g.db.query(Conversation).filter_by(session_id=session_id).first()
        conversation_id = conv.id if conv else None

        # Construir respuesta
        response = {
            "response": result['response'],
            "sources": result.get('sources', []),
            "context_used": result.get('context_used', False),
            "session_id": session_id,
            "conversation_id": conversation_id,  # ID numérico para continuar conversación
            "category": category,
            "intent": intent
        }

        # Guardar cache
        if len(response_cache) >= MAX_CACHE_SIZE:
            response_cache.pop(next(iter(response_cache)))
        response_cache[cache_key] = {
            "response": result['response'],
            "sources": result.get('sources', []),
            "context_used": result.get('context_used', False),
            "category": category,
            "intent": intent
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error en /ask: {e}", exc_info=True)
        return jsonify({"error": "Error procesando la consulta"}), 500

@chat_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """Endpoint para limpiar historial"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id') or request.headers.get('X-Session-ID')
        if not session_id:
            return jsonify({"error": "Se requiere session_id"}), 400

        # Crear instancia de SessionManager
        session_manager = SessionManager(db=g.db)
        
        # Verificar si el método clear_session existe, si no, crear uno alternativo
        if hasattr(session_manager, 'clear_session'):
            success = session_manager.clear_session(session_id)
        else:
            # Alternativa: buscar y eliminar la conversación
            from app.models.models import Conversation
            conv = session_manager.db.query(Conversation).filter_by(session_id=session_id).first()
            if conv:
                # ✅ Importamos Message al inicio del archivo, así que está disponible
                # Eliminar mensajes asociados primero
                session_manager.db.query(Message).filter_by(conversacion_id=conv.id).delete()
                # Eliminar conversación
                session_manager.db.delete(conv)
                session_manager.db.commit()
                success = True
            else:
                success = False
        
        if success:
            return jsonify({"message": "Historial limpiado correctamente", "session_id": session_id}), 200
        return jsonify({"error": "Sesión no encontrada"}), 404
    except Exception as e:
        logger.error(f"Error limpiando historial: {str(e)}")
        return jsonify({"error": "Error al limpiar historial"}), 500

@chat_bp.route('/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """Endpoint para obtener info de sesión"""
    try:
        session_manager = SessionManager(db=g.db)
        
        # Verificar si el método get_session_info existe
        if hasattr(session_manager, 'get_session_info'):
            info = session_manager.get_session_info(session_id)
        else:
            # Alternativa: información básica
            from app.models.models import Conversation
            conv = session_manager.db.query(Conversation).filter_by(session_id=session_id).first()
            if conv:
                # ✅ Importamos Message al inicio del archivo
                message_count = session_manager.db.query(Message).filter_by(conversacion_id=conv.id).count()
                info = {
                    "session_id": conv.session_id,
                    "usuario_id": conv.usuario_id,
                    "started_at": conv.started_at.isoformat() if conv.started_at else None,
                    "status": conv.status,
                    "message_count": message_count
                }
            else:
                info = None
        
        if info:
            return jsonify(info), 200
        return jsonify({"error": "Sesión no encontrada"}), 404
    except Exception as e:
        logger.error(f"Error obteniendo info de sesión: {str(e)}")
        return jsonify({"error": "Error al obtener información de sesión"}), 500

@chat_bp.route('/sessions/active', methods=['GET'])
def get_active_sessions():
    """Número de sesiones activas"""
    try:
        session_manager = SessionManager(db=g.db)
        
        # Verificar si los métodos existen
        if hasattr(session_manager, 'cleanup_expired_sessions'):
            session_manager.cleanup_expired_sessions()
        
        if hasattr(session_manager, 'get_active_sessions_count'):
            count = session_manager.get_active_sessions_count()
        else:
            # Alternativa: contar conversaciones activas
            from app.models.models import Conversation
            count = session_manager.db.query(Conversation).filter_by(status='activa').count()
        
        return jsonify({
            "active_sessions": count, 
            "cache_size": len(response_cache), 
            "services_status": "operational" if services_initialized else "degraded"
        }), 200
    except Exception as e:
        logger.error(f"Error obteniendo sesiones activas: {str(e)}")
        return jsonify({"error": "Error al obtener sesiones activas"}), 500

@chat_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Limpia cache de respuestas"""
    try:
        global response_cache
        response_cache = {}
        return jsonify({"message": "Cache limpiado correctamente"}), 200
    except Exception as e:
        logger.error(f"Error limpiando cache: {str(e)}")
        return jsonify({"error": "Error al limpiar cache"}), 500