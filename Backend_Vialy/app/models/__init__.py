"""
Inicialización de modelos y servicios
"""

import logging

logger = logging.getLogger(__name__)

# Variables globales
qa_chain = None
llm_model = None
classification_service = None
response_service = None

def initialize_services():
    """
    Inicializa todos los servicios
    Returns: bool - True si se inicializaron correctamente
    """
    global qa_chain, llm_model, classification_service, response_service
    
    try:
        logger.info("[INIT] 🚀 Iniciando servicios...")
        
        # 1. Crear cadena RAG con Ollama
        from app.rag.chain import create_chain
        
        logger.info("[INIT] Creando cadena RAG...")
        result = create_chain()
        
        # Verificar que sea una tupla de 2 elementos
        if not isinstance(result, tuple) or len(result) != 2:
            raise TypeError(
                f"create_chain() debe retornar (qa_chain, llm_model), "
                f"pero retornó: {type(result)}"
            )
        
        qa_chain, llm_model = result
        logger.info("[INIT] ✅ Cadena RAG y LLM creados")
        
        # 2. Inicializar servicios
        from app.services.classification_service import ClassificationService
        from app.services.response_service import ResponseService
        
        classification_service = ClassificationService(llm_model)
        response_service = ResponseService(qa_chain, llm_model)
        
        logger.info("[INIT] ✅ Servicios inicializados")
        logger.info("[INIT] 🎉 TODOS LOS SERVICIOS LISTOS")
        
        return True
        
    except Exception as e:
        logger.error(f"[INIT] ❌ Error: {str(e)}", exc_info=True)
        return False

def get_services():
    """
    Obtiene los servicios inicializados
    Returns: tuple o None
    """
    if all([qa_chain, llm_model, classification_service, response_service]):
        return qa_chain, llm_model, classification_service, response_service
    return None