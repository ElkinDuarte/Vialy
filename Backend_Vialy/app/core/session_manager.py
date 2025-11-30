"""
Módulo de gestión de sesiones de conversación.
Maneja el almacenamiento y recuperación de historiales de chat.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Gestor de sesiones de conversación"""
    
    def __init__(self, max_history: int = 5, session_timeout_hours: int = 24):
        """
        Inicializa el gestor de sesiones
        
        Args:
            max_history: Número máximo de mensajes a mantener en historial
            session_timeout_hours: Horas antes de que expire una sesión
        """
        self.conversations: Dict[str, Dict] = {}
        self.max_history = max_history
        self.session_timeout = timedelta(hours=session_timeout_hours)
        logger.info(f"SessionManager inicializado con max_history={max_history}")
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Crea una nueva sesión
        
        Args:
            session_id: ID de sesión opcional, se genera si no se proporciona
            
        Returns:
            str: ID de la sesión creada
        """
        if not session_id:
            session_id = str(uuid.uuid4())
        
        self.conversations[session_id] = {
            'messages': [],
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        logger.info(f"Nueva sesión creada: {session_id}")
        return session_id
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """
        Obtiene una sesión existente o crea una nueva
        
        Args:
            session_id: ID de sesión a buscar
            
        Returns:
            str: ID de la sesión
        """
        if session_id and session_id in self.conversations:
            # Actualizar última actividad
            self.conversations[session_id]['last_activity'] = datetime.now()
            return session_id
        
        return self.create_session(session_id)
    
    def add_message(self, session_id: str, user_message: str, assistant_message: str):
        """
        Agrega un par de mensajes al historial
        
        Args:
            session_id: ID de la sesión
            user_message: Mensaje del usuario
            assistant_message: Respuesta del asistente
        """
        if session_id not in self.conversations:
            self.create_session(session_id)
        
        self.conversations[session_id]['messages'].append({
            'user': user_message,
            'assistant': assistant_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Mantener solo los últimos N mensajes
        if len(self.conversations[session_id]['messages']) > self.max_history:
            self.conversations[session_id]['messages'] = \
                self.conversations[session_id]['messages'][-self.max_history:]
        
        self.conversations[session_id]['last_activity'] = datetime.now()
    
    def get_history(self, session_id: str, max_messages: Optional[int] = None) -> str:
        """
        Obtiene el historial formateado de una sesión
        
        Args:
            session_id: ID de la sesión
            max_messages: Número máximo de mensajes a retornar
            
        Returns:
            str: Historial formateado
        """
        if session_id not in self.conversations:
            return "Sin historial previo."
        
        messages = self.conversations[session_id]['messages']
        
        if not messages:
            return "Sin historial previo."
        
        # Limitar número de mensajes si se especifica
        if max_messages:
            messages = messages[-max_messages:]
        
        history = []
        for msg in messages:
            history.append(f"Usuario: {msg['user']}")
            history.append(f"Asistente: {msg['assistant']}")
        
        return "\n".join(history)
    
    def get_messages(self, session_id: str) -> List[Dict]:
        """
        Obtiene los mensajes completos de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            List[Dict]: Lista de mensajes
        """
        if session_id not in self.conversations:
            return []
        
        return self.conversations[session_id]['messages']
    
    def clear_session(self, session_id: str) -> bool:
        """
        Limpia el historial de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            bool: True si se limpió correctamente
        """
        if session_id in self.conversations:
            self.conversations[session_id]['messages'] = []
            logger.info(f"Historial limpiado para sesión: {session_id}")
            return True
        
        logger.warning(f"Sesión no encontrada: {session_id}")
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Elimina completamente una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            bool: True si se eliminó correctamente
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
            logger.info(f"Sesión eliminada: {session_id}")
            return True
        
        return False
    
    def cleanup_expired_sessions(self):
        """Elimina sesiones expiradas"""
        now = datetime.now()
        expired = []
        
        for session_id, session_data in self.conversations.items():
            last_activity = session_data.get('last_activity', session_data['created_at'])
            if now - last_activity > self.session_timeout:
                expired.append(session_id)
        
        for session_id in expired:
            self.delete_session(session_id)
        
        if expired:
            logger.info(f"Limpiadas {len(expired)} sesiones expiradas")
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        """
        Obtiene información de una sesión
        
        Args:
            session_id: ID de la sesión
            
        Returns:
            Dict: Información de la sesión o None
        """
        if session_id not in self.conversations:
            return None
        
        session = self.conversations[session_id]
        return {
            'session_id': session_id,
            'messages_count': len(session['messages']),
            'created_at': session['created_at'].isoformat(),
            'last_activity': session['last_activity'].isoformat()
        }
    
    def get_active_sessions_count(self) -> int:
        """
        Obtiene el número de sesiones activas
        
        Returns:
            int: Número de sesiones
        """
        return len(self.conversations)

# Instancia global del gestor de sesiones
session_manager = SessionManager()