from flask import Flask, request, jsonify
from flask_cors import CORS
from app.rag.chain import create_chain
import os
import logging
from dotenv import load_dotenv

# Configuración inicial
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Para caracteres especiales en español

# Configurar CORS
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Ajustar para producción
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Inicializar cadena QA y modelo LLM
qa_chain = None
llm_model = None

try:
    logger.info("[CHAIN] Iniciando cadena QA con Gemini...")
    qa_chain, llm_model = create_chain()
    logger.info("[CHAIN] ✅ Cadena QA inicializada correctamente")
except Exception as e:
    logger.error(f"[CHAIN] ⚠️ No se pudo inicializar la cadena QA: {str(e)}")

@app.route('/ask', methods=['POST'])
def ask_question():
    """Endpoint para realizar consultas sobre el código de tránsito"""
    if qa_chain is None or llm_model is None:
        return jsonify({
            "error": "Servicio no disponible. Intente más tarde."
        }), 503

    try:
        # Validar que venga JSON
        if not request.is_json:
            return jsonify({"error": "Se requiere Content-Type: application/json"}), 400
        
        data = request.get_json()
        
        # Validar campo query
        if 'query' not in data or not data['query']:
            return jsonify({"error": "El campo 'query' es requerido"}), 400
        
        query = data['query']
        logger.info(f"[ASK] Procesando pregunta: {query[:100]}...")

        # 1. Ejecutar RAG
        result = qa_chain.invoke({"query": query})
        source_docs = result.get("source_documents", [])
        has_sources = len(source_docs) > 0

        # 2. Preparar contexto
        formatted_sources = []
        context_texts = []
        for doc in source_docs:
            metadata = doc.metadata
            extracto = doc.page_content.strip().replace("\n", " ")
            context_texts.append(extracto)
            formatted_sources.append({
                "extracto": extracto[:300] + "...",
                "pagina": metadata.get("page_label") or metadata.get("page") or None,
                "archivo": os.path.basename(metadata.get("source", "documento_desconocido"))
            })

        # 3. Armar prompt híbrido
        joined_context = "\n\n".join(f"- {ctx}" for ctx in context_texts) if has_sources else "Sin contexto legal relevante."

        hybrid_prompt = f"""
        Eres un experto en tránsito colombiano. El usuario te hace la siguiente pregunta:

        \"{query}\"

        Te proporciono algunos fragmentos legales que podrían estar relacionados:

        {joined_context}

        Si alguno de los fragmentos contiene una respuesta directa o relacionada con la pregunta, úsala exactamente. 
        Si no hay información útil en los fragmentos, responde usando tu conocimiento general.

        Responde de forma clara, breve y útil, en máximo 6 líneas.
        Evita explicaciones largas o técnicas innecesarias.

        Respuesta:
        """

        logger.info("[PROMPT] Enviando prompt híbrido a Gemini...")
        response_text = llm_model.invoke(hybrid_prompt).content.strip()

        return jsonify({
            "response": response_text,
            "sources": formatted_sources,
            "context_used": has_sources
        }), 200

    except Exception as e:
        logger.error(f"❌ Error procesando pregunta: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Ocurrió un error al procesar tu pregunta. Por favor intenta nuevamente."
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({
        "status": "healthy" if qa_chain and llm_model else "degraded",
        "model": "gemini-2.0-flash",
        "ready": qa_chain is not None
    }), 200

@app.route('/', methods=['GET'])
def root():
    """Endpoint raíz con información de la API"""
    return jsonify({
        "message": "API del Código Nacional de Tránsito Colombiano 🇨🇴",
        "endpoints": {
            "documentación": "/docs",
            "salud": "/health",
            "consultas": "/ask (POST)"
        },
        "version": "1.0.0"
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Manejador para rutas no encontradas"""
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador para errores internos del servidor"""
    logger.error(f"Error interno: {str(error)}")
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )