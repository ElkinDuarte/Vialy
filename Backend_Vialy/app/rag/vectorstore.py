"""
Módulo de gestión del vectorstore FAISS
"""

import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from app.rag.loader import load_documents
from app.rag.splitter import split_documents

logger = logging.getLogger(__name__)

# Variable global para el vectorstore
vectorstore = None

def get_vectorstore():
    """
    Obtiene o crea el vectorstore FAISS
    
    Returns:
        FAISS: Vectorstore con documentos indexados
    """
    global vectorstore
    
    if vectorstore is not None:
        return vectorstore
    
    vector_db_path = os.getenv('VECTOR_DB_PATH', './vectorstore/faiss_index')
    
    # Verificar si ya existe el vectorstore
    if os.path.exists(vector_db_path):
        logger.info(f"Cargando vectorstore desde: {vector_db_path}")
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(
            vector_db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )
        logger.info("✅ Vectorstore cargado exitosamente")
        return vectorstore
    
    # Si no existe, crear uno nuevo
    logger.info("Vectorstore no encontrado. Creando uno nuevo...")
    vectorstore = create_vectorstore()
    return vectorstore

def get_embeddings():
    """
    Obtiene el modelo de embeddings
    
    Returns:
        HuggingFaceEmbeddings: Modelo de embeddings
    """
    model_name = os.getenv(
        'EMBEDDING_MODEL',
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    )
    
    logger.info(f"Cargando modelo de embeddings: {model_name}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    return embeddings

def create_vectorstore():
    """
    Crea un nuevo vectorstore desde los documentos
    
    Returns:
        FAISS: Vectorstore creado
    """
    logger.info("Iniciando creación de vectorstore...")
    
    # Cargar documentos
    documents = load_documents()
    
    if not documents:
        raise ValueError("No se encontraron documentos para indexar")
    
    logger.info(f"Documentos cargados: {len(documents)}")
    
    # Dividir documentos
    texts = split_documents(documents)
    logger.info(f"Textos divididos: {len(texts)}")
    
    # Crear embeddings
    embeddings = get_embeddings()
    
    # Crear vectorstore
    logger.info("Creando vectorstore FAISS...")
    vectorstore_new = FAISS.from_documents(texts, embeddings)
    
    # Guardar vectorstore
    vector_db_path = os.getenv('VECTOR_DB_PATH', './vectorstore/faiss_index')
    os.makedirs(os.path.dirname(vector_db_path), exist_ok=True)
    vectorstore_new.save_local(vector_db_path)
    
    logger.info(f"✅ Vectorstore guardado en: {vector_db_path}")
    
    return vectorstore_new