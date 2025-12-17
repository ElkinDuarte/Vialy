import os
import logging
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from app.config.settings import Config
from app.config.database import init_db, close_db, get_db
from app.routes.chat_routes import chat_bp
from app.routes.health_routes import health_bp
from app.routes.pdf_routes import pdf_bp
from app.routes.bd_routes import bd_routes
from app.core.session_manager import SessionManager

# Cargar variables de entorno
load_dotenv()

# Configurar logging
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

    # Inicializar JWT
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'clave_secreta_local')
    jwt = JWTManager(app)
    logger.info("✅ JWTManager inicializado")

    # Inicializar base de datos
    with app.app_context():
        logger.info("[INIT] Inicializando base de datos...")
        init_db()
        logger.info("[INIT] ✅ Base de datos lista")
        # Crear sesión de DB para SessionManager
        db_session = get_db()
        global session_manager
        session_manager = SessionManager(db=db_session)
        logger.info("✅ SessionManager inicializado con DB")

    # Registrar cleanup al shutdown
    @app.teardown_appcontext
    def cleanup(error=None):
        close_db()
        logger.info("[SHUTDOWN] Base de datos cerrada")

    # Registrar blueprints
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(bd_routes)

    logger.info("✅ Aplicación Flask inicializada correctamente")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=False  # Evitar reinicio automático
    )
