"""
Configuración y gestión de la base de datos.
Maneja las conexiones, inicialización de tablas y transacciones.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool, StaticPool
import logging

logger = logging.getLogger(__name__)

# Configuración de base de datos según entorno
DATABASE_URL = os.getenv(
    'DATABASE_URL'
)


engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verificar conexiones antes de usar (útil para conexiones largas)
    pool_recycle=3600,   # Reciclar conexiones cada hora para evitar timeouts
    echo=False
)

# Crear sesión factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def get_db():
    """
    Generador de dependencia para obtener sesión de base de datos.
    Uso en Flask: inyectar en rutas que lo necesiten.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    Llamar al startup de la aplicación.
    """
    from app.models.models import Base  # Ajusta la importación según tu estructura
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar base de datos: {str(e)}")
        raise


def close_db():
    """
    Cierra todas las conexiones de base de datos.
    Llamar al shutdown de la aplicación.
    """
    SessionLocal.remove()
    logger.info("Base de datos cerrada")