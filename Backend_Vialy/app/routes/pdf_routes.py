"""
Rutas para servir el PDF del Código de Tránsito
"""

import os
import logging
from flask import Blueprint, send_file, jsonify
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Crear blueprint
pdf_bp = Blueprint('pdf', __name__)

# Ruta de documentos
DOCUMENTS_PATH = os.getenv('DOCUMENTS_PATH')
# Nombre del PDF del código de tránsito
PDF_FILENAME = 'codigo_transito.pdf'

@pdf_bp.route('/pdf/codigo-transito', methods=['GET'])
@pdf_bp.route('/pdf/view/codigo_transito.pdf', methods=['GET'])
def view_codigo_transito():
    """Sirve el PDF del Código de Tránsito para visualización"""
    try:
        file_path = os.path.join(DOCUMENTS_PATH, PDF_FILENAME)
        
        if not os.path.exists(file_path):
            logger.error(f"PDF no encontrado en: {file_path}")
            return jsonify({
                "error": "Código de Tránsito no encontrado",
                "path": file_path
            }), 404
        
        # Servir el archivo PDF
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=False,
        )
        
    except Exception as e:
        logger.error(f"Error sirviendo PDF: {str(e)}")
        return jsonify({
            "error": "Error al servir el Código de Tránsito"
        }), 500

@pdf_bp.route('/pdf/download/codigo_transito.pdf', methods=['GET'])
def download_codigo_transito():
    """Descarga el PDF del Código de Tránsito"""
    try:
        file_path = os.path.join(DOCUMENTS_PATH, PDF_FILENAME)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "Código de Tránsito no encontrado"
            }), 404
        
        # Servir el archivo PDF para descarga
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='Codigo_Nacional_Transito_Colombia.pdf'
        )
        
    except Exception as e:
        logger.error(f"Error descargando PDF: {str(e)}")
        return jsonify({
            "error": "Error al descargar el Código de Tránsito"
        }), 500

@pdf_bp.route('/pdf/info', methods=['GET'])
def pdf_info():
    """Obtiene información del PDF del Código de Tránsito"""
    try:
        file_path = os.path.join(DOCUMENTS_PATH, PDF_FILENAME)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "Código de Tránsito no encontrado",
                "available": False
            }), 404
        
        # Obtener información básica
        file_size = os.path.getsize(file_path)
        
        # Intentar obtener número de páginas
        num_pages = None
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            num_pages = len(doc)
            doc.close()
        except:
            pass
        
        return jsonify({
            "available": True,
            "filename": PDF_FILENAME,
            "title": "Código Nacional de Tránsito Colombiano",
            "size_bytes": file_size,
            "size_mb": round(file_size / (1024 * 1024), 2),
            "num_pages": num_pages,
            "view_url": "/pdf/codigo-transito",
            "download_url": f"/pdf/download/{PDF_FILENAME}"
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo info de PDF: {str(e)}")
        return jsonify({
            "error": "Error al obtener información del PDF",
            "available": False
        }), 500
def list_pdfs():
    """Lista todos los PDFs disponibles"""
    try:
        if not os.path.exists(DOCUMENTS_PATH):
            return jsonify({
                "error": "Carpeta de documentos no encontrada",
                "pdfs": []
            }), 404
        
        # Listar archivos PDF
        files = os.listdir(DOCUMENTS_PATH)
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        
        # Obtener información de cada PDF
        pdfs_info = []
        for pdf_file in pdf_files:
            file_path = os.path.join(DOCUMENTS_PATH, pdf_file)
            file_size = os.path.getsize(file_path)
            
            pdfs_info.append({
                "filename": pdf_file,
                "display_name": pdf_file.replace('.pdf', '').replace('_', ' ').title(),
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "url": f"/pdf/view/{pdf_file}"
            })
        
        return jsonify({
            "pdfs": pdfs_info,
            "count": len(pdfs_info)
        }), 200
        
    except Exception as e:
        logger.error(f"Error listando PDFs: {str(e)}")
        return jsonify({
            "error": "Error al listar PDFs"
        }), 500

@pdf_bp.route('/pdf/view/<filename>', methods=['GET'])
def view_pdf(filename):
    """Sirve un PDF para visualización"""
    try:
        # Sanitizar nombre de archivo
        filename = secure_filename(filename)
        
        if not filename.lower().endswith('.pdf'):
            return jsonify({
                "error": "El archivo debe ser un PDF"
            }), 400
        
        file_path = os.path.join(DOCUMENTS_PATH, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "PDF no encontrado"
            }), 404
        
        # Servir el archivo PDF
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=False,  # Para visualizar en el navegador
        )
        
    except Exception as e:
        logger.error(f"Error sirviendo PDF: {str(e)}")
        return jsonify({
            "error": "Error al servir PDF"
        }), 500

@pdf_bp.route('/pdf/download/<filename>', methods=['GET'])
def download_pdf(filename):
    """Descarga un PDF"""
    try:
        # Sanitizar nombre de archivo
        filename = secure_filename(filename)
        
        if not filename.lower().endswith('.pdf'):
            return jsonify({
                "error": "El archivo debe ser un PDF"
            }), 400
        
        file_path = os.path.join(DOCUMENTS_PATH, filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "error": "PDF no encontrado"
            }), 404
        
        # Servir el archivo PDF para descarga
        return send_file(
            file_path,
            mimetype='application/pdf',
            as_attachment=True,  # Para descargar
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error descargando PDF: {str(e)}")
        return jsonify({
            "error": "Error al descargar PDF"
        }), 500