"""
Servicio de generación de respuestas.
Maneja la lógica de generación de respuestas usando RAG y prompts especializados.
"""

import logging
import os
from typing import Dict, List, Tuple
from app.core.prompts import PromptTemplates

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
        Obtiene contexto usando RAG
        
        Args:
            query: Pregunta del usuario
            
        Returns:
            Tuple[List[Dict], str]: (fuentes formateadas, contexto en texto)
        """
        try:
            # Ejecutar RAG
            result = self.qa_chain.invoke({"query": query})
            source_docs = result.get("source_documents", [])
            
            # Preparar fuentes formateadas
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
            
            # Crear contexto en texto
            if context_texts:
                joined_context = "\n\n".join(f"- {ctx}" for ctx in context_texts)
            else:
                joined_context = "Sin contexto legal relevante."
            
            logger.info(f"RAG encontró {len(source_docs)} documentos relevantes")
            return formatted_sources, joined_context
            
        except Exception as e:
            logger.error(f"Error en RAG: {str(e)}", exc_info=True)
            return [], "Sin contexto legal relevante."
    
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
            # Obtener el prompt apropiado
            prompt = PromptTemplates.get_response_prompt(
                category=category,
                query=query,
                context=context,
                history=history
            )
            
            logger.info(f"Generando respuesta con prompt de categoría: {category}")
            
            # Generar respuesta
            response = self.llm_model.invoke(prompt).content.strip()
            
            logger.info("Respuesta generada exitosamente")
            return response
            
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