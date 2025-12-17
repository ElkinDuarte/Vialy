"""
Servicio de clasificación de consultas.
VERSIÓN OPTIMIZADA: Solo usa keywords, sin llamadas al LLM.
"""

import logging
import re
from typing import Tuple
from functools import lru_cache

logger = logging.getLogger(__name__)

class ClassificationService:
    """Servicio para clasificar consultas de usuarios - SOLO KEYWORDS"""
    
    # Palabras clave AMPLIADAS para mejor clasificación
    KEYWORDS = {
        'MULTA': [
            'multa', 'sanción', 'penalización', 'cuánto', 'cuesta', 'valor',
            'infracción', 'comparendo', 'pagar', 'cuanto cuesta', 'precio',
            'costo', 'fotomulta', 'sancionado', 'penalizado', 'castigo',
            'sanciones', 'infracciones', 'comparendos'
        ],
        'REQUISITO': [
            'documento', 'requisito', 'necesito', 'tramite', 'permiso',
            'llevar', 'presentar', 'documentos', 'requisitos', 'papeles',
            'certificado', 'licencia', 'soat', 'seguro', 'tarjeta',
            'necesarios', 'obligatorio', 'debo llevar', 'que necesito'
        ],
        'NORMATIVA': [
            'ley', 'artículo', 'norma', 'código', 'dice', 'establece',
            'legal', 'articulo', 'artículo', 'legislación', 'reglamento',
            'normativa', 'permitido', 'prohibido', 'puede', 'debo',
            'obligatorio', 'está prohibido', 'se permite'
        ],
        'PROCEDIMIENTO': [
            'cómo', 'pasos', 'proceso', 'renovar', 'obtener', 'hacer',
            'dónde', 'donde', 'trámite', 'procedimiento', 'solicitar',
            'como hacer', 'como obtener', 'como renovar', 'gestionar',
            'realizar', 'efectuar', 'adelantar', 'como se hace'
        ]
    }
    
    def __init__(self, llm_model=None):
        """
        Inicializa el servicio de clasificación
        
        Args:
            llm_model: Modelo LLM (no se usa en esta versión)
        """
        self.llm_model = llm_model
        logger.info("ClassificationService inicializado (modo KEYWORDS)")
    
    @lru_cache(maxsize=512)
    def _quick_classify(self, query_lower: str) -> str:
        """
        Clasificación rápida basada en palabras clave
        
        Args:
            query_lower: Query en minúsculas
            
        Returns:
            str: Categoría detectada
        """
        scores = {category: 0 for category in self.KEYWORDS.keys()}
        
        # Contar coincidencias de keywords
        for category, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in query_lower:
                    scores[category] += 1
        
        # Obtener la categoría con más coincidencias
        max_score = max(scores.values())
        
        if max_score > 0:
            # Retornar la categoría con más coincidencias
            for category, score in scores.items():
                if score == max_score:
                    return category
        
        # Si no hay coincidencias, es GENERAL
        return 'GENERAL'
    
    def classify_query(self, query: str) -> str:
        """
        Clasifica una consulta en una categoría usando SOLO keywords
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            str: Categoría (MULTA, REQUISITO, NORMATIVA, PROCEDIMIENTO, GENERAL)
        """
        try:
            query_lower = query.lower()
            
            # Usar SOLO clasificación rápida (sin LLM)
            category = self._quick_classify(query_lower)
            
            logger.info(f"✅ Clasificación rápida: {category}")
            return category
            
        except Exception as e:
            logger.error(f"Error en clasificación: {str(e)}", exc_info=True)
            return 'GENERAL'
    
    def get_intent(self, query: str) -> int:
        """
        Determina la intención del usuario (simplificado - sin LLM)
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            int: Intención (1=Información, 2=Explicación, 3=Asesoría)
        """
        try:
            query_lower = query.lower()
            
            # Clasificación rápida de intención por keywords
            # Asesoría (3)
            if any(word in query_lower for word in [
                'cómo', 'como', 'pasos', 'proceso', 'debo', 'debería',
                'me conviene', 'qué hago', 'que hago', 'ayuda'
            ]):
                return 3
            
            # Explicación (2)
            elif any(word in query_lower for word in [
                'qué es', 'que es', 'por qué', 'por que', 'explica',
                'funciona', 'significa', 'diferencia', 'cuál es', 'cual es'
            ]):
                return 2
            
            # Información específica (1) - default
            else:
                return 1
            
        except Exception as e:
            logger.error(f"Error en análisis de intención: {str(e)}", exc_info=True)
            return 1
    
    def analyze_query(self, query: str) -> Tuple[str, int]:
        """
        Analiza completamente una consulta (sin llamadas al LLM)
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            Tuple[str, int]: (categoría, intención)
        """
        category = self.classify_query(query)
        intent = self.get_intent(query)
        
        logger.info(f"📊 Análisis: Categoría={category}, Intención={intent}")
        return category, intent