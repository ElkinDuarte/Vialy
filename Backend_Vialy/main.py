import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.chat_routes import chat_bp
from app.routes.health_routes import health_bp
from app.config.settings import Config

# Configuración inicial
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurar CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-Session-ID"],
            "supports_credentials": True
        }
    })
    
    # Registrar blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)
    
    logger.info("✅ Aplicación Flask inicializada correctamente")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 8000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )