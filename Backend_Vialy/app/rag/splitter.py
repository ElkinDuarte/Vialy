# app/rag/splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

def split_documents(documents: List[Document]) -> List[Document]:
    """Divide documentos en chunks más pequeños."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=250,
        chunk_overlap=40,
        length_function=len,
        separators=[
            "\nArtículo ", "\nARTÍCULO ", "\nArt. ", 
            "\nParágrafo", "\n", ".", " "
        ],
        add_start_index=True
    )
    chunks = splitter.split_documents(documents)
    print(f"[SPLITTER] {len(chunks)} chunks generados.")
    return chunks
