"""
Módulo para crear la cadena RAG con Gemini
"""

import os
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

def create_chain():
    """
    Crea la cadena RAG y el modelo LLM
    
    Returns:
        tuple: (qa_chain, llm_model)
        
    Raises:
        ValueError: Si GOOGLE_API_KEY no está configurada
    """
    
    # Verificar que GOOGLE_API_KEY esté configurada
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain.chains import RetrievalQA
        from app.rag.vectorstore import get_vectorstore
        
        logger.info("Inicializando modelo Gemini...")
        
        # Configurar modelo
        model_name = os.getenv('MODEL_NAME', 'gemini-2.0-flash')
        temperature = float(os.getenv('TEMPERATURE', '0.3'))
        
        llm_model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature
        )
        
        logger.info("Cargando vectorstore...")
        vectorstore = get_vectorstore()
        
        logger.info("Creando cadena QA...")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": int(os.getenv('TOP_K_DOCUMENTS', '3'))}
            ),
            return_source_documents=True
        )
        
        logger.info("✅ Cadena RAG creada exitosamente")
        return qa_chain, llm_model
        
    except Exception as e:
        logger.error(f"Error creando cadena RAG: {str(e)}", exc_info=True)
        raise