"""
--------------------------------------------------
Smart Research Assistant
Centralized Configuration File
--------------------------------------------------
"""

# APPLICATION
APP_NAME = "Smart Research Assistant"
APP_VERSION = "1.0"
AUTHOR = "Dinesh Kumar"

# LLM
LLM_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 2048
QUERY_TEMPERATURE = 0.0

# EMBEDDINGS
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# CHUNKING
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CONTEXT_CHARACTERS = 8000

# RETRIEVAL
TOP_K = 5
INITIAL_K = 10
SEARCH_TYPE = "similarity"
ENABLE_MULTI_QUERY = True
ENABLE_HISTORY = True
ENABLE_QUERY_ANALYTICS = True

# CHROMADB
CHROMA_DIRECTORY = "database/chroma"
COLLECTION_NAME = "research_assistant"
RESET_COLLECTION = False
PERSIST_DIRECTORY = True

# FILES
UPLOAD_DIRECTORY = "uploads"
SUPPORTED_FILES = ["pdf", "txt", "docx"]

# EVALUATION
ENABLE_RAGAS = True
ENABLE_CONFIDENCE_SCORE = True
ENABLE_SOURCE_CITATIONS = True

# ANALYTICS
ENABLE_ANALYTICS = True
TRACK_RESPONSE_TIME = True

# STREAMLIT
PAGE_TITLE = "Smart Research Assistant"
PAGE_ICON = "📚"
LAYOUT = "wide"

# EVALUATION WEIGHTS
RAGAS_WEIGHT = 0.4
RETRIEVAL_WEIGHT = 0.3
SOURCE_WEIGHT = 0.2
RESPONSE_WEIGHT = 0.1  # Weights must sum up to exactly 1.0
MINIMUM_RESPONSE_LENGTH = 20  # Characters below which RAGAS evaluation is skipped

# PIPELINE FALLBACKS
INSUFFICIENT_CONTEXT_RESPONSE = "I could not find sufficient information in the uploaded documents to answer this question."
