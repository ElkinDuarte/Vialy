"""
Servicio de generación de respuestas.
Maneja la lógica de generación de respuestas usando RAG y prompts especializados.
"""

import logging
import os
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class ResponseService:
    """Servicio para generar respuestas inteligentes"""
    
    def __init__(self, qa_chain, llm_model):
        """
        Inicializa el servicio de respuestas
        
        Args:
            qa_chain: Cadena RAG para búsqueda de contexto
            llm_model: Modelo LLM para generación de respuestas
        """
        self.qa_chain = qa_chain
        self.llm_model = llm_model
        logger.info("ResponseService inicializado")
    
    def get_rag_context(self, query: str) -> Tuple[List[Dict], str]:
        """
        Obtiene contexto usando el sistema RAG
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            Tuple[List[Dict], str]: (fuentes formateadas, contexto en texto)
        """
        try:
            # Usar el sistema RAG mejorado si está disponible
            if hasattr(self.llm_model, 'rag_system'):
                return self._get_improved_rag_context(query)
            # Usar el sistema RAG legacy (qa_chain)
            return self._legacy_rag_search(query)
            
        except Exception as e:
            logger.error(f"Error en RAG: {str(e)}", exc_info=True)
            return [], "Sin contexto legal relevante."
    
    def _get_improved_rag_context(self, query: str) -> Tuple[List[Dict], str]:
        """Obtiene contexto usando el sistema RAG mejorado"""
        try:
            rag_results = self.llm_model.rag_system.query(query, k=3)
            
            formatted_sources = []
            context_parts = []
            
            for result in rag_results:
                content = result.get("content", "").strip()
                metadata = result.get("metadata", {})
                
                if not content:
                    continue
                    
                # Extraer información de la fuente
                source_info = {
                    'extracto': content[:300] + "...",
                    'source': metadata.get('source', 'Código Nacional de Tránsito'),
                    'page': metadata.get('page', 'N/A')
                }
                formatted_sources.append(source_info)
                
                # Limpiar y formatear el contenido
                cleaned_content = self._clean_rag_content(content)
                if cleaned_content:
                    context_parts.append(cleaned_content)
            
            # Unir las partes relevantes del contexto
            context = "\n\n".join(context_parts) if context_parts else "No se encontró información específica."
            
            logger.info(f"RAG mejorado procesó {len(context_parts)} fragmentos")
            return formatted_sources, context
            
        except Exception as e:
            logger.error(f"Error en RAG mejorado: {str(e)}", exc_info=True)
            return [], "No se pudo obtener la información solicitada."
    
    def _legacy_rag_search(self, query: str) -> Tuple[List[Dict], str]:
        """Obtiene contexto usando qa_chain (método legacy)"""
        try:
            # Ejecutar búsqueda con qa_chain
            result = self.qa_chain.invoke({"query": query})
            source_docs = result.get("source_documents", [])
            
            # Formatear fuentes
            formatted_sources = []
            context_texts = []
            
            for doc in source_docs:
                metadata = doc.metadata
                content = doc.page_content.strip().replace("\n", " ")
                context_texts.append(content)
                
                formatted_sources.append({
                    "extracto": content[:300] + "...",
                    "pagina": metadata.get("page_label") or metadata.get("page"),
                    "archivo": os.path.basename(metadata.get("source", "documento"))
                })
            
            # Crear contexto
            context = "\n\n".join(f"- {ctx}" for ctx in context_texts) if context_texts else "Sin contexto."
            
            logger.info(f"RAG legacy encontró {len(source_docs)} documentos")
            return formatted_sources, context
            
        except Exception as e:
            logger.error(f"Error en RAG legacy: {str(e)}", exc_info=True)
            return [], "Sin contexto legal relevante."
    
    def _clean_rag_content(self, content: str) -> str:
        """Limpia y formatea el contenido del RAG"""
        # Eliminar saltos de línea y espacios múltiples
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Filtrar líneas irrelevantes (números de página, etc.)
        filtered_lines = []
        skip_terms = ['capítulo', 'página', 'hoja', 'página de']
        
        for line in lines:
            # Saltar líneas muy cortas o que contengan términos irrelevantes
            if len(line) < 10:
                continue
            if any(term in line.lower() for term in skip_terms):
                continue
            filtered_lines.append(line)
        
        # Unir y limpiar
        cleaned = ' '.join(' '.join(filtered_lines).split())
        
        # Limitar longitud
        if len(cleaned) > 800:
            cleaned = cleaned[:800] + "..."
            
        return cleaned
    
    def generate_response(
        self,
        query: str,
        category: str,
        history: str,
        context: str
    ) -> str:
        """
        Genera una respuesta usando el prompt especializado
        
        Args:
            query: Pregunta del usuario
            category: Categoría de la consulta
            history: Historial de conversación
            context: Contexto del RAG
            
        Returns:
            str: Respuesta generada
        """
        try:
            # Importar prompts (intentar versión mejorada primero)
            try:
                from app.core.prompts_rapidos import PromptTemplates
                # Versión mejorada: usa 'rag_context' en lugar de 'context'
                prompt = PromptTemplates.get_response_prompt(
                    category=category,
                    query=query,
                    rag_context=context,  # Parámetro correcto para prompts_mejorado
                    history=history,
                    conversation_context=""  # Opcional
                )
            except ImportError:
                # Fallback a versión antigua
                from app.core.prompts import PromptTemplates
                prompt = PromptTemplates.get_response_prompt(
                    category=category,
                    query=query,
                    context=context,  # Versión antigua usa 'context'
                    history=history
                )
            
            logger.info(f"Generando respuesta con prompt de categoría: {category}")
            
            # Generar respuesta
            response = self.llm_model.invoke(prompt)
            
            # Extraer texto de la respuesta
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            response_text = response_text.strip()
            
            logger.info(f"Respuesta generada: {len(response_text)} caracteres")
            return response_text
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {str(e)}", exc_info=True)
            raise
    
    def process_query(
        self,
        query: str,
        category: str,
        history: str
    ) -> Dict:
        """
        Procesa una consulta completa (RAG + generación de respuesta)
        
        Args:
            query: Pregunta del usuario
            category: Categoría de la consulta
            history: Historial de conversación
            
        Returns:
            Dict: Respuesta con sources y metadata
        """
        try:
            # Obtener contexto con RAG
            formatted_sources, context = self.get_rag_context(query)
            
            # Generar respuesta
            response_text = self.generate_response(
                query=query,
                category=category,
                history=history,
                context=context
            )
            
            return {
                "response": response_text,
                "sources": formatted_sources,
                "context_used": len(formatted_sources) > 0
            }
            
        except Exception as e:
            logger.error(f"Error procesando consulta: {str(e)}", exc_info=True)
            raise