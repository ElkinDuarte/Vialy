"""
Gestión de sesiones de conversación asociadas a un usuario.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
from sqlalchemy.orm import Session
from app.models.models import Conversation, Message
from app.config.database import SessionLocal

logger = logging.getLogger(__name__)

class SessionManager:
    """Gestor de sesiones con BD, cada sesión asociada a un usuario"""
    
    def __init__(self, max_history: int = 5, session_timeout_hours: int = 24, db: Optional[Session] = None):
        self.max_history = max_history
        self.session_timeout = timedelta(hours=session_timeout_hours)
        self.db = db or SessionLocal()
        logger.info(f"SessionManager inicializado (max_history={max_history}, BD={'sí' if db else 'no'})")
    
    def get_or_create_session(self, usuario_id: int, session_id: Optional[str] = None) -> str:
        """
        Obtiene o crea una sesión para un usuario.
        Args:
            usuario_id: ID del usuario (obligatorio)
            session_id: ID de sesión existente (opcional)
        Returns:
            str: ID de la sesión
        """
        if usuario_id is None:
            raise ValueError("usuario_id es obligatorio para crear una sesión")
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        try:
            conv = self.db.query(Conversation).filter_by(session_id=session_id).first()
            if not conv:
                # Crear nueva conversación asociada al usuario
                conv = Conversation(
                    session_id=session_id,
                    usuario_id=usuario_id,
                    started_at=datetime.utcnow(),
                    status='activa'
                )
                self.db.add(conv)
                self.db.commit()
                logger.info(f"✅ Nueva conversación creada: {session_id} (usuario_id={usuario_id})")
            else:
                conv.updated_at = datetime.utcnow()
                self.db.commit()
            return session_id
        except Exception as e:
            logger.error(f"❌ Error creando sesión: {str(e)}")
            self.db.rollback()
            return session_id

    def add_message(self, session_id: str, user_message: str, assistant_message: str, category: Optional[str] = None):
        """Agrega mensajes a la conversación"""
        try:
            conv = self.db.query(Conversation).filter_by(session_id=session_id).first()
            if not conv:
                logger.warning(f"Conversación {session_id} no encontrada")
                return
            
            # CORREGIDO: Usar los nombres correctos de los campos
            user_msg = Message(
                conversacion_id=conv.id, 
                sender='usuario',  # Cambiado de 'role' a 'sender'
                message=user_message  # Cambiado de 'content' a 'message'
            )
            assistant_msg = Message(
                conversacion_id=conv.id, 
                sender='chatbot',  # Cambiado de 'role' a 'sender'
                message=assistant_message  # Cambiado de 'content' a 'message'
            )
            self.db.add_all([user_msg, assistant_msg])
            
            # Actualizar la conversación
            conv.ended_at = None  # Mantener activa
            conv.status = 'activa'
            
            self.db.commit()
            logger.info(f"✅ Mensajes guardados en {session_id}")
        except Exception as e:
            logger.error(f"❌ Error guardando mensajes: {str(e)}")
            self.db.rollback()

    def get_history(self, session_id: str, max_messages: Optional[int] = None) -> str:
        """
        Obtiene el historial de una conversación como texto formateado.
        
        Args:
            session_id: ID de la sesión
            max_messages: Número máximo de mensajes a recuperar
            
        Returns:
            str: Historial formateado o mensaje de error
        """
        try:
            # Buscar la conversación por session_id
            conv = self.db.query(Conversation).filter_by(session_id=session_id).first()
            if not conv:
                return "Sin historial."
            
            # Consultar los mensajes de esta conversación
            query = self.db.query(Message).filter_by(conversacion_id=conv.id).order_by(Message.created_at.asc())
            
            # Limitar si se especifica max_messages
            if max_messages:
                query = query.limit(max_messages)
            
            messages = query.all()
            
            if not messages:
                return "Sin historial previo."
            
            # Formatear el historial
            history_lines = []
            for msg in messages:
                sender = "Usuario" if msg.sender == 'usuario' else "Asistente"
                # Limitar longitud para no hacerlo muy largo
                content_preview = msg.message[:100] + "..." if len(msg.message) > 100 else msg.message
                history_lines.append(f"{sender}: {content_preview}")
            
            return "\n".join(history_lines)
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo historial para sesión {session_id}: {str(e)}", exc_info=True)
            return "Error recuperando historial."
# Instancia global
session_manager = SessionManager()
