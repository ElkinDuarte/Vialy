from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import logging

logger = logging.getLogger(__name__)

def split_documents(documents: List[Document]) -> List[Document]:
    """Divide documentos en chunks más pequeños."""
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=[
                "\nArtículo ", "\nARTÍCULO ", "\nArt. ", 
                "\nParágrafo", "\n\n", "\n", ".", " ", ""
            ],
            add_start_index=True
        )
        chunks = splitter.split_documents(documents)
        logger.info(f"📄 {len(chunks)} chunks generados")
        return chunks
    except Exception as e:
        logger.error(f"Error al dividir documentos: {str(e)}")
        raise