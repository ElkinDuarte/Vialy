"""
Prompts OPTIMIZADOS para velocidad
Versión reducida para respuestas más rápidas
"""

class PromptTemplates:
    """Templates de prompts optimizados para velocidad"""
    
    # Clasificación (mantener igual)
    CLASIFICACION = """Clasifica esta pregunta en UNA categoría:
MULTA, REQUISITO, NORMATIVA, PROCEDIMIENTO, GENERAL

Pregunta: "{query}"

Categoría:"""

    INTENCION = """Intención (1=info, 2=explicación, 3=asesoría):
"{query}"
Número:"""

    # Prompts SIMPLIFICADOS para respuestas rápidas
    
    RESPUESTA_MULTA = """Experto en multas de tránsito Colombia.

Pregunta: "{query}"

Información disponible:
{rag_context}

Valores 2025:
- Tipo C = $711,750 (15 SMLDV)
- Tipo D = $1,423,500 (30 SMLDV)

Responde en máximo 4 líneas con valor exacto y artículo."""

    RESPUESTA_REQUISITO = """Experto en requisitos de tránsito Colombia.

Pregunta: "{query}"

Info: {rag_context}

Lista los documentos/requisitos necesarios. Máximo 4 líneas."""

    RESPUESTA_NORMATIVA = """Experto en normativa de tránsito Colombia.

Pregunta: "{query}"

Información: {rag_context}

Explica la norma citando el artículo. Máximo 4 líneas."""

    RESPUESTA_PROCEDIMIENTO = """Experto en trámites de tránsito Colombia.

Pregunta: "{query}"

Info: {rag_context}

Lista los pasos necesarios. Máximo 4 líneas."""

    RESPUESTA_GENERAL = """Asistente de tránsito Colombia.

Pregunta: "{query}"

Info: {rag_context}

Responde de forma útil. Máximo 3 líneas."""

    @classmethod
    def get_classification_prompt(cls, query: str) -> str:
        return cls.CLASIFICACION.format(query=query)
    
    @classmethod
    def get_intention_prompt(cls, query: str) -> str:
        return cls.INTENCION.format(query=query)
    
    @classmethod
    def get_response_prompt(cls, category: str, query: str, rag_context: str, 
                           history: str = "", conversation_context: str = "") -> str:
        """
        Versión SIMPLIFICADA - ignora history y conversation_context para velocidad
        """
        prompt_map = {
            'MULTA': cls.RESPUESTA_MULTA,
            'REQUISITO': cls.RESPUESTA_REQUISITO,
            'NORMATIVA': cls.RESPUESTA_NORMATIVA,
            'PROCEDIMIENTO': cls.RESPUESTA_PROCEDIMIENTO,
            'GENERAL': cls.RESPUESTA_GENERAL
        }
        
        template = prompt_map.get(category, cls.RESPUESTA_GENERAL)
        
        return template.format(
            query=query,
            rag_context=rag_context[:1000] if rag_context else "Sin info específica."
        )


CATEGORIES = ['MULTA', 'REQUISITO', 'NORMATIVA', 'PROCEDIMIENTO', 'GENERAL']

CATEGORY_NAMES = {
    'MULTA': 'Multas',
    'REQUISITO': 'Requisitos',
    'NORMATIVA': 'Normativa',
    'PROCEDIMIENTO': 'Procedimientos',
    'GENERAL': 'General'
}