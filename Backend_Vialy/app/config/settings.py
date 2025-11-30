import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-cambiar-en-produccion')
    JSON_AS_ASCII = False
    
    # Sesiones
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # API
    API_VERSION = "2.0.0"
    API_TITLE = "API del Código Nacional de Tránsito Colombiano"
    
    # Google/Gemini
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-2.0-flash-exp')
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.3'))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))
    
    # RAG
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vectorstore/faiss_index')
    DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH', './documents')
    TOP_K_DOCUMENTS = int(os.getenv('TOP_K_DOCUMENTS', '3'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    
    # Embeddings
    EMBEDDING_MODEL = os.getenv(
        'EMBEDDING_MODEL',
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    )
    
    # Conversación
    MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', '5'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Debug
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    
class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True

# Diccionario de configuraciones
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name='default'):
    """Obtiene la configuración según el nombre"""
    return config_by_name.get(config_name, DevelopmentConfig)