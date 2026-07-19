"""
Smart Research Assistant
Embedding Management Layer

Responsibilities
----------------
1. Embedding Generation
2. Model Management
3. Embedding Validation
4. Analytics Support
5. Dimension Extraction
6. Error Handling
"""
from typing import Dict
from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL, EMBEDDING_DIMENSIONS

# GLOBAL EMBEDDING MODEL
EMBEDDING_INSTANCE = None

# EMBEDDING MODEL
def get_embedding_model():
    """Initializes the embedding model only once and reuses it throughout the project."""
    global EMBEDDING_INSTANCE
    try:
        if EMBEDDING_INSTANCE is None:
            EMBEDDING_INSTANCE = HuggingFaceEmbeddings(
                model_name=f"sentence-transformers/{EMBEDDING_MODEL}",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
        return EMBEDDING_INSTANCE
    except Exception as error:
        raise RuntimeError(f"Embedding initialization failed : {error}")

# EMBEDDING DIMENSIONS
def get_embedding_dimensions():
    """Returns embedding dimensions."""
    return EMBEDDING_DIMENSIONS

# EMBEDDING VALIDATION
def validate_embedding_model():
    """Performs sanity checks on embedding generation."""
    try:
        model = get_embedding_model()
        sample_embedding = model.embed_query("Testing Embeddings")
        
        if not sample_embedding or len(sample_embedding) != EMBEDDING_DIMENSIONS:
            return False
        return True
    except Exception:
        return False

# ANALYTICS SUPPORT
def get_embedding_statistics():
    """Returns embedding statistics for the analytics dashboard."""
    return {
        "model_name": EMBEDDING_MODEL,
        "dimensions": EMBEDDING_DIMENSIONS,
        "normalized": True,
        "api_dependency": False
    }

# DEBUGGING SUPPORT
def generate_sample_embedding():
    """Used only for debugging."""
    model = get_embedding_model()
    return model.embed_query("Artificial Intelligence")[:10]

"""
Future Improvements
-------------------
1. BGE Embeddings
2. E5 Embeddings
3. Hybrid Embeddings
4. Azure Embeddings
5. OpenAI Embeddings
6. Cross Encoder Reranking
7. Hybrid Retrieval
"""
