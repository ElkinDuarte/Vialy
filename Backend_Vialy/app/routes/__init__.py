from .chat_routes import chat_bp
from .health_routes import health_bp
from .pdf_routes import pdf_bp
from .bd_routes import bd_routes

__all__ = ['chat_bp', 'health_bp', 'pdf_bp','bd_routes']