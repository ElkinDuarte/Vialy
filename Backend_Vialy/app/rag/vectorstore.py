# app/rag/vectorstore.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from langchain.schema import Document

def create_vectorstore(docs: List[Document]) -> FAISS:
    """Crea un vectorstore FAISS con embeddings optimizados para texto legal en español."""

    if not docs:
        raise ValueError("No se proporcionaron documentos para indexar en FAISS.")

    try:
        print("[VECTORSTORE] Usando embeddings BGE-M3 (óptimo para español y leyes)...")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


        vectorstore = FAISS.from_documents(docs, embeddings)
        print("[VECTORSTORE] Vectorstore FAISS creado correctamente.")
        return vectorstore

    except Exception as e:
        raise RuntimeError(f"Error al crear el vectorstore: {str(e)}")
