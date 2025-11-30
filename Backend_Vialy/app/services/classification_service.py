"""
Servicio de clasificación de consultas.
Analiza y categoriza las preguntas de los usuarios.
"""

import logging
import re
from typing import Tuple
from functools import lru_cache
from app.core.prompts import PromptTemplates, CATEGORIES

logger = logging.getLogger(__name__)

class ClassificationService:
    """Servicio para clasificar consultas de usuarios"""
    
    # Palabras clave para clasificación rápida
    KEYWORDS = {
        'MULTA': ['multa', 'sanción', 'penalización', 'cuánto', 'infracción', 'comparendo', 'pagar'],
        'REQUISITO': ['documento', 'requisito', 'necesito', 'tramite', 'permiso', 'llevar', 'presentar'],
        'NORMATIVA': ['ley', 'artículo', 'norma', 'código', 'dice', 'establece', 'legal'],
        'PROCEDIMIENTO': ['cómo', 'pasos', 'proceso', 'renovar', 'obtener', 'hacer', 'dónde']
    }
    
    def __init__(self, llm_model):
        """
        Inicializa el servicio de clasificación
        
        Args:
            llm_model: Modelo LLM para clasificación
        """
        self.llm_model = llm_model
        logger.info("ClassificationService inicializado")
    
    @lru_cache(maxsize=256)
    def _quick_classify(self, query_lower: str) -> str:
        """
        Clasificación rápida basada en palabras clave (sin LLM)
        
        Args:
            query_lower: Query en minúsculas
            
        Returns:
            str: Categoría probable o None
        """
        scores = {category: 0 for category in self.KEYWORDS.keys()}
        
        for category, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[category] += 1
        
        max_score = max(scores.values())
        if max_score > 0:
            # Retornar la categoría con más coincidencias
            for category, score in scores.items():
                if score == max_score:
                    return category
        
        return None
    
    def classify_query(self, query: str) -> str:
        """
        Clasifica una consulta en una categoría
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            str: Categoría (MULTA, REQUISITO, NORMATIVA, PROCEDIMIENTO, GENERAL)
        """
        try:
            query_lower = query.lower()
            
            # OPTIMIZACIÓN: Primero intentar clasificación rápida
            quick_result = self._quick_classify(query_lower)
            if quick_result:
                logger.info(f"Clasificación rápida: {quick_result}")
                return quick_result
            
            # Si no hay coincidencias claras, usar LLM
            prompt = PromptTemplates.get_classification_prompt(query)
            response = self.llm_model.invoke(prompt).content.strip().upper()
            
            # Validar que la respuesta sea una categoría válida
            if response in CATEGORIES:
                logger.info(f"Consulta clasificada (LLM) como: {response}")
                return response
            
            logger.warning(f"Categoría inválida recibida: {response}, usando GENERAL")
            return 'GENERAL'
            
        except Exception as e:
            logger.error(f"Error en clasificación: {str(e)}", exc_info=True)
            return 'GENERAL'
    
    def get_intent(self, query: str) -> int:
        """
        Determina la intención del usuario (simplificado)
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            int: Intención (1=Información, 2=Explicación, 3=Asesoría)
        """
        try:
            query_lower = query.lower()
            
            # OPTIMIZACIÓN: Clasificación rápida de intención
            if any(word in query_lower for word in ['cómo', 'pasos', 'proceso', 'debo']):
                return 3  # Asesoría
            elif any(word in query_lower for word in ['qué es', 'por qué', 'explica', 'funciona']):
                return 2  # Explicación
            else:
                return 1  # Información específica
            
        except Exception as e:
            logger.error(f"Error en análisis de intención: {str(e)}", exc_info=True)
            return 1
    
    def analyze_query(self, query: str) -> Tuple[str, int]:
        """
        Analiza completamente una consulta
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            Tuple[str, int]: (categoría, intención)
        """
        category = self.classify_query(query)
        intent = self.get_intent(query)
        
        logger.info(f"Análisis completo - Categoría: {category}, Intención: {intent}")
        return category, intent