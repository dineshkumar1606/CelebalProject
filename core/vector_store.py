"""
--------------------------------------------------
Knowledge Base(Vector Store)
Responsibilities
----------------
1. Collection Management
2. Persistent Storage
3. Document Indexing
4. Embedding Generation
5. Collection Analytics
6. Duplicate Detection
7. Collection Management
8. Error Handling
-------------------------------------------------
"""
from typing import Dict, List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from config import CHROMA_DIRECTORY, COLLECTION_NAME
from core.embeddings import get_embedding_model
from core.chunking import generate_chunk_id

# DATABASE INITIALIZATION
def initialize_database():
    """Initializes ChromaDB."""
    try:
        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=CHROMA_DIRECTORY,
            embedding_function=get_embedding_model()
        )
        return vector_store
    except Exception as error:
        raise RuntimeError(f"Unable to initialize ChromaDB : {error}")

# ADD DOCUMENTS
def add_documents(chunks: List[Document]):
    """Adds chunks to the collection with uniquely generated structural IDs."""
    vector_store = initialize_database()
    ids = []
    
    for index, chunk in enumerate(chunks):
        ids.append(generate_chunk_id(chunk, index))
        
    vector_store.add_documents(documents=chunks, ids=ids)
    return vector_store

# COLLECTION STATS
def get_collection_statistics():
    """Returns collection statistics."""
    vector_store = initialize_database()
    collection = vector_store.get()
    return {
        "total_chunks": len(collection["ids"]),
        "collection_name": COLLECTION_NAME,
        "persistent_storage": True,
        "embedding_model": "MiniLM"
    }

# DOCUMENT EXISTENCE
def document_exists(document_id: str) -> bool:
    """Checks whether document exists."""
    vector_store = initialize_database()
    results = vector_store.get(where={"document_id": document_id})
    return len(results["ids"]) > 0

# DELETE DOCUMENT
def delete_document(document_id: str):
    """Deletes specific document."""
    vector_store = initialize_database()
    results = vector_store.get(where={"document_id": document_id})
    if results["ids"]:
        vector_store.delete(ids=results["ids"])

# RESET COLLECTION
def reset_database():
    """Deletes entire collection chunks using LangChain API."""
    vector_store = initialize_database()
    collection = vector_store.get()
    if collection["ids"]:
        vector_store.delete(ids=collection["ids"])

# RETURN VECTOR STORE
def get_vector_store():
    """Returns initialized vector database."""
    return initialize_database()

# RESET COLLECTION VIA CLIENT
def reset_collection():
    """Deletes collection completely via the underlying database client wrapper."""
    try:
        vector_store = initialize_database()
        # Accesses the native persistent chromadb client exposed by LangChain Chroma
        vector_store._client.delete_collection(COLLECTION_NAME)
        print("\nCollection Reset Successfully.")
    except Exception as error:
        print(f"\nFailed to reset collection: {error}")

"""
Future Improvements
-------------------
Hybrid Retrieval
pgvector
Milvus
Azure AI Search
Distributed Storage
Multi Collection Support
Cross Encoder Reranking
"""
