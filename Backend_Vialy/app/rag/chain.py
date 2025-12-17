"""
Módulo para crear la cadena RAG con Ollama
Adaptado para usar rag_system.py en lugar de vectorstore.py
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def create_chain():
    """
    Crea la cadena RAG y el modelo LLM usando Ollama
    
    Returns:
        tuple: (qa_chain, llm_model)
    """
    
    try:
        logger.info("[CHAIN] 🚀 Iniciando creación de cadena RAG con Ollama...")
        
        # 1. Importar Ollama
        try:
            from langchain_ollama import OllamaLLM
            logger.info("[CHAIN] Usando langchain-ollama (actualizado)")
        except ImportError:
            from langchain_community.llms import Ollama as OllamaLLM
            logger.warning("[CHAIN] Usando langchain_community.llms.Ollama (deprecated)")
            logger.warning("[CHAIN] Considera instalar: pip install langchain-ollama")
        
        from langchain.chains import RetrievalQA
        
        # 2. Configuración
        model_name = os.getenv('OLLAMA_MODEL', 'mistral')
        base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        temperature = float(os.getenv('TEMPERATURE', '0.3'))
        num_ctx = int(os.getenv('OLLAMA_NUM_CTX', '8192'))
        num_predict = int(os.getenv('OLLAMA_NUM_PREDICT', '512'))
        
        logger.info(f"[CHAIN] Configuración:")
        logger.info(f"  • Modelo: {model_name}")
        logger.info(f"  • URL: {base_url}")
        logger.info(f"  • Contexto: {num_ctx} tokens")
        
        # 3. Crear modelo
        llm_model = OllamaLLM(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
            num_ctx=num_ctx,
            num_predict=num_predict,
            repeat_penalty=1.1,
            top_k=40,
            top_p=0.9,
        )
        
        logger.info("[CHAIN] ✅ Modelo Ollama creado")
        
        # 4. Verificar conexión
        try:
            logger.info("[CHAIN] Verificando conexión con Ollama...")
            test_response = llm_model.invoke("test", stop=[])
            logger.info("[CHAIN] ✅ Conexión verificada exitosamente")
        except Exception as e:
            error_msg = str(e)
            
            if "404" in error_msg or "not found" in error_msg.lower():
                raise ConnectionError(
                    f"El modelo '{model_name}' no está instalado.\n"
                    f"Descárgalo con: ollama pull {model_name}"
                )
            elif "connect" in error_msg.lower():
                raise ConnectionError(
                    f"No se puede conectar con Ollama en {base_url}\n"
                    f"Inicia Ollama: ollama serve"
                )
            else:
                raise ConnectionError(f"Error: {error_msg}")
        
        # 5. Cargar sistema RAG (intentar diferentes nombres de módulos)
        rag_system = None
        vectorstore = None
        
        # Intento 1: Usando rag_system.py
        try:
            from app.rag.rag_system import RAGSystem
            logger.info("[CHAIN] Cargando RAG usando rag_system.py...")
            rag_system = RAGSystem()
            vectorstore = rag_system.vectorstore
            logger.info("[CHAIN] ✅ RAG System cargado")
        except (ImportError, AttributeError) as e:
            logger.warning(f"[CHAIN] No se pudo cargar rag_system.py: {e}")
        
        # Intento 2: Usando vectorstore.py
        if vectorstore is None:
            try:
                from app.rag.vectorstore import get_vectorstore
                logger.info("[CHAIN] Cargando vectorstore.py...")
                vectorstore = get_vectorstore()
                logger.info("[CHAIN] ✅ Vectorstore cargado")
            except ImportError as e:
                logger.warning(f"[CHAIN] No se pudo cargar vectorstore.py: {e}")
        
        # Si no se pudo cargar ninguno, error
        if vectorstore is None:
            raise ImportError(
                "No se pudo cargar el sistema RAG.\n"
                "Asegúrate de tener app/rag/rag_system.py o app/rag/vectorstore.py"
            )
        
        # 6. Crear cadena QA
        logger.info("[CHAIN] Creando cadena de QA...")
        
        top_k = int(os.getenv('TOP_K_DOCUMENTS', '3'))
        
        # Obtener retriever del vectorstore
        if hasattr(vectorstore, 'as_retriever'):
            retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        elif hasattr(vectorstore, 'get_retriever'):
            retriever = vectorstore.get_retriever(k=top_k)
        else:
            raise AttributeError("Vectorstore no tiene método as_retriever o get_retriever")
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        logger.info("[CHAIN] ✅ Cadena QA creada exitosamente")
        logger.info(f"[CHAIN] 🎉 Sistema listo con {model_name}")
        
        # 7. Retornar tupla
        return qa_chain, llm_model
        
    except ImportError as e:
        logger.error(f"[CHAIN] Error de importación: {e}")
        raise
    except Exception as e:
        logger.error(f"[CHAIN] ❌ Error: {str(e)}", exc_info=True)
        raise


def get_llm_model():
    """
    Crea solo el modelo LLM sin la cadena RAG
    
    Returns:
        OllamaLLM: Instancia del modelo
    """
    try:
        try:
            from langchain_ollama import OllamaLLM
        except ImportError:
            from langchain_community.llms import Ollama as OllamaLLM
        
        model_name = os.getenv('OLLAMA_MODEL', 'mistral')
        base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        temperature = float(os.getenv('TEMPERATURE', '0.3'))
        
        llm_model = OllamaLLM(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
            num_ctx=int(os.getenv('OLLAMA_NUM_CTX', '8192')),
            num_predict=int(os.getenv('OLLAMA_NUM_PREDICT', '512'))
        )
        
        # Verificar
        llm_model.invoke("test", stop=[])
        
        return llm_model
        
    except Exception as e:
        logger.error(f"Error creando modelo LLM: {e}")
        raise