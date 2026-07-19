import uuid
from typing import List
from typing import Dict
from langchain_core.documents import Document
from langchain_text_splitters import (RecursiveCharacterTextSplitter)
from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)
import hashlib
#                TEXT SPLITTER
def get_text_splitter():
    """
    Returns configured text splitter.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        length_function=len,
        is_separator_regex=False
    )
#               CHUNK CREATION
def create_chunks(
        documents: List[Document]
) -> List[Document]:
    """
    Creates chunks from documents.
    """
    splitter = get_text_splitter()
    chunks = splitter.split_documents(
        documents
    )
    chunks = add_chunk_metadata(
        chunks
    )
    validate_chunks(
        chunks
    )
    return chunks
#              METADATA PRESERVATION
def add_chunk_metadata(
        chunks: List[Document]
) -> List[Document]:
    """
    Preserves metadata required by
    downstream modules.
    """
    total_chunks = len(chunks)
    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_number"] = (
            index + 1
        )
        chunk.metadata["total_chunks"] = (
            total_chunks
        )
        chunk.metadata["chunk_id"] = (
            str(uuid.uuid4())
        )
    return chunks

def generate_chunk_id(chunk,chunk_number:int):
    """
    Generates deterministic
    chunk ids.
    """
    source = chunk.metadata.get(
        "source",
        "unknown"
    )
    page = chunk.metadata.get(
        "page",
        0
    )

    content = (
        f"{source}"
        f"{page}"
        f"{chunk_number}"
        f"{chunk.page_content}"
    )
    return hashlib.sha256(
        content.encode()
    ).hexdigest()
#               CHUNK VALIDATION
def validate_chunks(
        chunks: List[Document]
) -> None:
    """
    Validates generated chunks.
    """
    if not chunks:
        raise ValueError(
            "No chunks were generated."
        )
    for chunk in chunks:
        if not chunk.page_content.strip():
            raise ValueError(
                "Empty chunk generated."
            )
#             CHUNK STATISTICS
def get_chunk_statistics(
        chunks: List[Document]
) -> Dict:
    """
    Returns statistics required by
    analytics dashboard.
    """
    total_characters = sum(
        len(chunk.page_content)
        for chunk in chunks
    )
    total_chunks = len(chunks)
    average_chunk_size = round(
        total_characters /
        max(1, total_chunks),
        2
    )
    return {
        "total_chunks":
        total_chunks,
        "chunk_size":
        CHUNK_SIZE,
        "chunk_overlap":
        CHUNK_OVERLAP,
        "average_chunk_size":
        average_chunk_size,
        "total_characters":
        total_characters
    }
#               DEBUGGING
def display_chunk_sample(
        chunks: List[Document]
) -> str:
    """
    Returns first chunk for debugging.
    """
    if not chunks:
        return "No chunks generated."
    return chunks[0].page_content[:500]


"""
 Future Improvements   
Semantic Chunking

Token Based Chunking

Adaptive Chunk Sizes

Hybrid Chunking

Parent Document Retrieval

Contextual Compression
    """