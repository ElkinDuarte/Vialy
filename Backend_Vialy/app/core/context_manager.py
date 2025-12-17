"""
Gestor de contexto de conversación para mantener coherencia.
Rastrea temas, infracciones, artículos citados y preguntas principales.
"""

import logging
from typing import Dict, List, Optional, Set
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Conversation, ConversationContext, Message

logger = logging.getLogger(__name__)

# Diccionario de palabras clave por categoría
CATEGORY_KEYWORDS = {
    'MULTA': ['multa', 'sanción', 'infracción', 'penalización', 'castigo', 'pena', 'valor', 'pagar', 'costo'],
    'REQUISITO': ['requisito', 'documento', 'documentación', 'licencia', 'soat', 'cedula', 'identidad', 'trámite'],
    'NORMATIVA': ['artículo', 'ley', 'código', 'norma', 'decreto', 'resolución', 'reglamento'],
    'PROCEDIMIENTO': ['cómo', 'pasos', 'proceso', 'tramite', 'obtener', 'renovar', 'solicitar', 'hacer'],
    'CONDUCCION': ['conducir', 'manejar', 'velocidad', 'seguridad', 'precaución', 'luz', 'freno', 'señal']
}

# Infracciones comunes y sus códigos de artículo
COMMON_INFRACTIONS = {
    'exceso_velocidad': {'article': '29', 'category': 'MULTA', 'keywords': ['exceso', 'velocidad', 'rápido', 'límite']},
    'sin_licencia': {'article': 'D.1', 'category': 'MULTA', 'keywords': ['licencia', 'sin', 'no tiene']},
    'no_usar_cinturon': {'article': '6', 'category': 'MULTA', 'keywords': ['cinturón', 'cinturon', 'seguridad']},
    'semaforo_rojo': {'article': 'D.4', 'category': 'MULTA', 'keywords': ['semáforo', 'rojo', 'roja', 'luz roja']},
    'sin_soat': {'article': 'D.2', 'category': 'MULTA', 'keywords': ['soat', 'seguro']},
    'celular': {'article': '38', 'category': 'MULTA', 'keywords': ['celular', 'telefono', 'teléfono', 'mano']},
    'estacionamiento': {'article': '2', 'category': 'MULTA', 'keywords': ['estacionar', 'estacionamiento', 'parqueo', 'aparcar']},
}


class ConversationContextManager:
    """Gestor de contexto de conversación"""
    
    def __init__(self, db: Session):
        """
        Inicializa el gestor de contexto
        
        Args:
            db: Sesión de base de datos SQLAlchemy
        """
        self.db = db
    
    def get_or_create_context(self, conversation_id: str) -> ConversationContext:
        """
        Obtiene o crea contexto para una conversación
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            ConversationContext: Contexto de la conversación
        """
        context = self.db.query(ConversationContext).filter_by(
            conversation_id=conversation_id
        ).first()
        
        if not context:
            context = ConversationContext(conversation_id=conversation_id)
            self.db.add(context)
            self.db.commit()
        
        return context
    
    def update_context(self, conversation_id: str, user_message: str, assistant_message: str,
                      category: str, sources: List[Dict] = None):
        """
        Actualiza el contexto basado en un nuevo par de mensajes
        
        Args:
            conversation_id: ID de la conversación
            user_message: Mensaje del usuario
            assistant_message: Respuesta del asistente
            category: Categoría detectada
            sources: Fuentes RAG utilizadas
        """
        context = self.get_or_create_context(conversation_id)
        conversation = self.db.query(Conversation).get(conversation_id)
        
        # Actualizar tema principal
        if not context.topics:
            context.topics = []
        
        # Agregar categoría a topics
        category_lower = category.lower()
        if category_lower not in context.topics:
            context.topics.append(category_lower)
        
        # Detectar infracciones mencionadas
        self._detect_infractions(context, user_message)
        
        # Detectar artículos citados
        self._detect_articles(context, assistant_message)
        
        # Actualizar tema principal de conversación
        if not conversation.primary_topic:
            conversation.primary_topic = category
        
        # Agregar a preguntas principales
        if len(user_message.split()) > 3:  # Solo si es pregunta substancial
            if not context.main_questions:
                context.main_questions = []
            
            # Agregar si no existe una pregunta similar
            user_query_normalized = user_message.lower().strip()
            if not any(q.lower() == user_query_normalized for q in context.main_questions):
                context.main_questions.append(user_message)
                # Mantener solo las últimas 5 preguntas principales
                context.main_questions = context.main_questions[-5:]
        
        # Almacenar respuesta clave
        if assistant_message and len(assistant_message) > 20:
            if not context.key_answers:
                context.key_answers = []
            
            context.key_answers.append({
                'question': user_message,
                'answer': assistant_message[:500],  # Primeros 500 caracteres
                'category': category,
                'timestamp': datetime.utcnow().isoformat()
            })
            # Mantener solo las últimas 10 respuestas clave
            context.key_answers = context.key_answers[-10:]
        
        context.updated_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"Contexto actualizado para conversación {conversation_id}")
    
    def _detect_infractions(self, context: ConversationContext, message: str):
        """
        Detecta infracciones mencionadas en un mensaje
        
        Args:
            context: Contexto de conversación
            message: Mensaje a analizar
        """
        message_lower = message.lower()
        
        for infraction_key, infraction_data in COMMON_INFRACTIONS.items():
            for keyword in infraction_data['keywords']:
                if keyword in message_lower:
                    if infraction_key not in context.infractions_mentioned:
                        context.infractions_mentioned.append(infraction_key)
    
    def _detect_articles(self, context: ConversationContext, message: str):
        """
        Detecta artículos citados en un mensaje
        
        Args:
            context: Contexto de conversación
            message: Mensaje a analizar
        """
        # Patrón simple para detectar "Artículo XXX"
        import re
        
        # Buscar patrones como "Artículo 29", "Art. 131", "artículo D.1"
        patterns = [
            r'Artículo\s+([A-D]?\d+(?:\.\d+)?)',
            r'Art\.\s+([A-D]?\d+(?:\.\d+)?)',
            r'artículo\s+([A-D]?\d+(?:\.\d+)?)',
            r'art\.\s+([A-D]?\d+(?:\.\d+)?)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                if match not in context.articles_cited:
                    context.articles_cited.append(match)
    
    def get_formatted_context(self, conversation_id: str, max_items: int = 5) -> str:
        """
        Obtiene el contexto formateado para incluir en prompts
        
        Args:
            conversation_id: ID de la conversación
            max_items: Número máximo de items a incluir
            
        Returns:
            str: Contexto formateado
        """
        context = self.get_or_create_context(conversation_id)
        conversation = self.db.query(Conversation).get(conversation_id)
        
        parts = []
        
        # Tema principal
        if conversation and conversation.primary_topic:
            parts.append(f"📌 Tema Principal: {conversation.primary_topic}")
        
        # Temas tratados
        if context.topics:
            parts.append(f"🏷️ Temas: {', '.join(context.topics)}")
        
        # Infracciones mencionadas
        if context.infractions_mentioned:
            infraction_names = []
            for inf_key in context.infractions_mentioned[:max_items]:
                if inf_key in COMMON_INFRACTIONS:
                    name = inf_key.replace('_', ' ').title()
                    infraction_names.append(name)
            if infraction_names:
                parts.append(f"⚠️ Infracciones Mencionadas: {', '.join(infraction_names)}")
        
        # Artículos citados
        if context.articles_cited:
            articles = ', '.join(context.articles_cited[:max_items])
            parts.append(f"📜 Artículos: {articles}")
        
        # Preguntas principales
        if context.main_questions:
            parts.append("❓ Preguntas Principales:")
            for q in context.main_questions[-3:]:
                parts.append(f"  • {q}")
        
        return "\n".join(parts) if parts else "Sin contexto previo."
    
    def should_provide_context(self, conversation_id: str) -> bool:
        """
        Determina si el contexto debe incluirse en el prompt
        
        Args:
            conversation_id: ID de la conversación
            
        Returns:
            bool: True si hay contexto relevante
        """
        context = self.db.query(ConversationContext).filter_by(
            conversation_id=conversation_id
        ).first()
        
        if not context:
            return False
        
        # Incluir contexto si hay más de 2 mensajes o hay infracciones/artículos detectados
        return len(context.topics) > 0 or len(context.infractions_mentioned) > 0
