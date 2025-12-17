from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import logging

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        try:
            # Embeddings locales
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # 📌 RUTA CORRECTA AL PDF
            BASE_DIR = os.path.dirname(__file__)      # app/rag
            PDF_PATH = os.path.join(BASE_DIR, "data", "codigo_transito.pdf")

            if not os.path.exists(PDF_PATH):
                raise FileNotFoundError(f"PDF no encontrado: {PDF_PATH}")

            # Cargar PDF
            loader = PyPDFLoader(PDF_PATH)
            documents = loader.load()

            # Split
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = splitter.split_documents(documents)

            # Vectorstore
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)

            logger.info(f"✅ RAG cargado con {len(chunks)} fragmentos")

        except Exception as e:
            logger.error(f"❌ Error al inicializar RAGSystem: {e}")
            raise

    def retrieve(self, query: str, k: int = 3) -> str:
        docs = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join(d.page_content for d in docs)
