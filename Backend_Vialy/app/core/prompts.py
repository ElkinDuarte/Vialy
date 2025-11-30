"""
Módulo de gestión de prompts para el sistema de respuestas.
Contiene todos los templates de prompts organizados por categoría.
"""

class PromptTemplates:
    """Clase que contiene todos los templates de prompts"""
    
    # Prompt para clasificación de consultas
    CLASIFICACION = """Analiza la siguiente pregunta y clasifícala en una de estas categorías:
- MULTA: Si pregunta sobre sanciones, multas, infracciones, penalizaciones
- REQUISITO: Si pregunta sobre documentos, requisitos, trámites, permisos
- NORMATIVA: Si pregunta sobre leyes, artículos, normas, regulaciones
- PROCEDIMIENTO: Si pregunta sobre cómo hacer algo, pasos a seguir
- GENERAL: Si es una pregunta general o no cae en las anteriores

Pregunta: "{query}"

Responde SOLO con la categoría en mayúsculas (MULTA, REQUISITO, NORMATIVA, PROCEDIMIENTO, o GENERAL)."""

    # Prompt para análisis de intención
    INTENCION = """Analiza la intención del usuario en esta pregunta:
Pregunta: "{query}"

¿El usuario está preguntando sobre:
1. Información específica (quiere datos concretos)
2. Explicación (quiere entender cómo funciona algo)
3. Asesoría (quiere consejo o guía)

Responde SOLO con el número (1, 2, o 3)."""

    # Prompt especializado para MULTAS
    RESPUESTA_MULTA = """Eres un experto en el Código Nacional de Tránsito Colombiano especializado en sanciones y multas.

Pregunta del usuario: "{query}"

Contexto legal disponible:
{context}

Historial de la conversación:
{history}

INSTRUCCIONES CRÍTICAS:
1. Las multas se calculan en SMLDV (Salarios Mínimos Legales DIARIOS Vigentes)
2. SMLDV 2025 = $47,450 pesos (SMMLV / 30)
3. Tipos de multas según Artículo 131:
   - Tipo A = 4 SMLDV = $189,800 COP (vehículos no automotores)
   - Tipo B = 8 SMLDV = $379,600 COP (infracciones leves)
   - Tipo C = 15 SMLDV = $711,750 COP (infracciones moderadas)
   - Tipo D = 30 SMLDV = $1,423,500 COP (infracciones graves)
   - Tipo E = 45 SMLDV = $2,135,250 COP (infracciones muy graves)

4. Infracciones comunes:
   - Exceso de velocidad (C.29): Tipo C = $711,750
   - Conducir sin licencia (D.1): Tipo D = $1,423,500 + inmovilización
   - No usar cinturón (C.6): Tipo C = $711,750
   - Semáforo en rojo (D.4): Tipo D = $1,423,500
   - Sin SOAT (D.2): Tipo D = $1,423,500 + inmovilización
   - Celular sin manos libres (C.38): Tipo C = $711,750
   - Estacionar prohibido (C.2): Tipo C = $711,750
   - Sin licencia en porta (B.1): Tipo B = $379,600

5. SIEMPRE menciona:
   - El valor EXACTO en pesos colombianos
   - El tipo de multa y número de artículo
   - SMLDV correspondiente
   - Otras sanciones si aplican (inmovilización, suspensión)

6. NUNCA digas "no tengo información" - usa los datos proporcionados
7. Si el contexto no tiene detalles, usa los valores estándar del Artículo 131

Formato de respuesta:
"Según el Artículo 131 ([numeral]), [infracción] tiene una multa tipo [X] equivalente a $[VALOR] pesos colombianos ([Y] SMLDV). [Otras sanciones si aplican]."

Respuesta (máximo 6 líneas):"""

    # Prompt especializado para REQUISITOS
    RESPUESTA_REQUISITO = """Eres un experto en el Código Nacional de Tránsito Colombiano especializado en requisitos y documentación.

Pregunta del usuario: "{query}"

Contexto legal disponible:
{context}

Historial de la conversación:
{history}

INSTRUCCIONES CRÍTICAS:
1. SIEMPRE da respuestas CONCRETAS y específicas
2. Lista EXACTAMENTE los documentos requeridos
3. Si mencionas costos, usa valores actualizados (2025)
4. NO digas "consulta la página web" o "verifica con autoridades"

Documentos obligatorios para conducir en Colombia:
- Licencia de conducción vigente
- Documento de identidad (cédula)
- SOAT vigente
- Certificado de revisión técnico-mecánica (si aplica)
- Tarjeta de propiedad del vehículo

Costos aproximados (2025):
- SOAT: $350,000 - $800,000 (varía según vehículo)
- Licencia nueva: $350,000 - $500,000
- Renovación licencia: $200,000 - $300,000
- Revisión técnico-mecánica: $70,000 - $150,000

Formato de respuesta: Lista clara y numerada con toda la información necesaria.

Respuesta (máximo 6 líneas):"""

    # Prompt especializado para NORMATIVA
    RESPUESTA_NORMATIVA = """Eres un experto en el Código Nacional de Tránsito Colombiano especializado en normativa.

Pregunta del usuario: "{query}"

Contexto legal disponible:
{context}

Historial de la conversación:
{history}

Instrucciones:
- Cita el artículo o ley específica si está en el contexto
- Explica la norma de forma clara
- Menciona excepciones si existen
- Se preciso y conciso, máximo 6 líneas
- Si no hay información en el contexto, usa tu conocimiento general

Respuesta:"""

    # Prompt especializado para PROCEDIMIENTOS
    RESPUESTA_PROCEDIMIENTO = """Eres un experto en el Código Nacional de Tránsito Colombiano especializado en procedimientos.

Pregunta del usuario: "{query}"

Contexto legal disponible:
{context}

Historial de la conversación:
{history}

Instrucciones:
- Describe los pasos de forma numerada si es posible
- Se claro y práctico
- Menciona dónde realizar el trámite si está en el contexto
- Se conciso, máximo 6 líneas
- Si no hay información en el contexto, usa tu conocimiento general

Respuesta:"""

    # Prompt general
    RESPUESTA_GENERAL = """Eres un asistente experto en el Código Nacional de Tránsito Colombiano.

Pregunta del usuario: "{query}"

Contexto legal disponible:
{context}

Historial de la conversación:
{history}

Instrucciones:
- Responde de forma clara y útil
- Si el contexto tiene información relevante, úsala
- Se conciso, máximo 6 líneas
- Si no hay información en el contexto, usa tu conocimiento general

Respuesta:"""

    @classmethod
    def get_classification_prompt(cls, query: str) -> str:
        """Obtiene el prompt de clasificación formateado"""
        return cls.CLASIFICACION.format(query=query)
    
    @classmethod
    def get_intention_prompt(cls, query: str) -> str:
        """Obtiene el prompt de intención formateado"""
        return cls.INTENCION.format(query=query)
    
    @classmethod
    def get_response_prompt(cls, category: str, query: str, context: str, history: str) -> str:
        """
        Obtiene el prompt de respuesta según la categoría
        
        Args:
            category: Categoría de la consulta (MULTA, REQUISITO, etc.)
            query: Pregunta del usuario
            context: Contexto del RAG
            history: Historial de conversación
            
        Returns:
            str: Prompt formateado
        """
        prompt_map = {
            'MULTA': cls.RESPUESTA_MULTA,
            'REQUISITO': cls.RESPUESTA_REQUISITO,
            'NORMATIVA': cls.RESPUESTA_NORMATIVA,
            'PROCEDIMIENTO': cls.RESPUESTA_PROCEDIMIENTO,
            'GENERAL': cls.RESPUESTA_GENERAL
        }
        
        template = prompt_map.get(category, cls.RESPUESTA_GENERAL)
        return template.format(query=query, context=context, history=history)

# Constantes de categorías
CATEGORIES = ['MULTA', 'REQUISITO', 'NORMATIVA', 'PROCEDIMIENTO', 'GENERAL']

# Mapeo de categorías a nombres amigables
CATEGORY_NAMES = {
    'MULTA': 'Sanciones y Multas',
    'REQUISITO': 'Requisitos y Documentación',
    'NORMATIVA': 'Normativa Legal',
    'PROCEDIMIENTO': 'Procedimientos y Trámites',
    'GENERAL': 'Consulta General'
}