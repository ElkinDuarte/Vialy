from langchain_community.vectorstores import Chroma
from langchain import Document
from services import EmbeddingService
from config import Config
from typing import List, Dict

class VectorStoreService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.embeddings = self.embedding_service.get_embeddings()
        self.vector_store = None
    
    def create_vector_store_from_chunks(self, chunks: List[Dict]):
        """Crea un vector store a partir de chunks procesados"""
        # Convertir chunks a documentos de LangChain
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk['text'],
                metadata=chunk['metadata']
            )
            documents.append(doc)
        
        print(f"Creando vector store con {len(documents)} documentos...")
        
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=Config.VECTOR_STORE_PATH
        )
        self.vector_store.persist()
        
        print("Vector store creado y persistido exitosamente!")
        return self.vector_store
    
    def load_vector_store(self):
        """Carga un vector store existente"""
        self.vector_store = Chroma(
            persist_directory=Config.VECTOR_STORE_PATH,
            embedding_function=self.embeddings
        )
        return self.vector_store
    
    def search(self, query: str, k: int = 4, filter_dict: Dict = None):
        """Busca documentos similares con filtros opcionales"""
        if not self.vector_store:
            self.load_vector_store()
        
        if filter_dict:
            results = self.vector_store.similarity_search(
                query, 
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search(query, k=k)
        
        return results
    
    def search_by_article(self, article_number: str, k: int = 1):
        """Busca un artículo específico por número"""
        return self.search(
            f"Artículo {article_number}",
            k=k,
            filter_dict={'article_number': article_number}
        )