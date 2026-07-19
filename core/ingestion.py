"""
--------------------------------------------------
Smart Research Assistant
Document Ingestion Layer

Responsibilities
----------------
1. Document Validation
2. Document Loading
3. Chunk Creation
4. Knowledge Base Indexing
5. Analytics Generation
6. Graceful Failure Handling
--------------------------------------------------
"""
from typing import Dict, List

from core.loader import load_document, get_document_statistics
from core.chunking import create_chunks, get_chunk_statistics
from core.vector_store import add_documents, get_collection_statistics
#          SINGLE DOCUMENT PROCESSING
def process_document(file_path: str) -> Dict:
    """Processes a single document."""
    documents = load_document(file_path)
    chunks = create_chunks(documents)
    add_documents(chunks)

    return {
        "documents": documents,
        "chunks": chunks,
        "status": "SUCCESS"
    }
#            MULTIPLE DOCUMENTS
def process_documents(file_paths: List[str]) -> Dict:
    """Processes multiple documents."""
    total_documents = 0
    total_chunks = 0
    failed_documents = []

    for file_path in file_paths:
        try:
            results = process_document(file_path)
            total_documents += len(results["documents"])
            total_chunks += len(results["chunks"])
        except Exception:
            failed_documents.append(file_path)

    collection_stats = get_collection_statistics()

    return {
        "documents": total_documents,
        "chunks": total_chunks,
        "failed": len(failed_documents),
        "failed_documents": failed_documents,
        "collection": collection_stats,
        "status": "SUCCESS"
    }
#             ANALYTICS SUPPORT
def get_ingestion_statistics(report: Dict) -> Dict:
    """Returns analytics required by Streamlit."""
    return {
        "documents": report["documents"],
        "chunks": report["chunks"],
        "failed": report["failed"],
        "collection_name": report["collection"]["collection_name"]
    }
