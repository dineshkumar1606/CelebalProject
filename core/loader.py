"""
--------------------------------------------------
Smart Research Assistant
Document Management Layer
Responsibilities:
-----------------
1. File Validation
2. Document Loading
3. Metadata Preservation
4. Document Statistics
5. Duplicate Detection
6. Content Validation
7. Error Handling
--------------------------------------------------
"""
import os
import hashlib
from typing import List, Dict
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)
from config import SUPPORTED_FILES
#                 CUSTOM EXCEPTIONS
class UnsupportedFileError(Exception):
    pass

class EmptyDocumentError(Exception):
    pass

class CorruptedDocumentError(Exception):
    pass
#                 VALIDATION
def validate_document(file_path: str) -> None:
    """
    Validates file extension and existence.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"'{file_path}' does not exist."
        )
    extension = file_path.split(".")[-1].lower()
    if extension not in SUPPORTED_FILES:
        raise UnsupportedFileError(
            f"Unsupported file format : {extension}\n"
            f"Supported formats : {SUPPORTED_FILES}"
        )
def validate_content(documents: List[Document]) -> None:
    """
    Checks whether any text has been extracted.
    """
    if not documents:
        raise EmptyDocumentError(
            "No document was loaded."
        )
    extracted_text = ""
    for document in documents:
        extracted_text += document.page_content.strip()
    if not extracted_text:
        raise EmptyDocumentError(
            "No text could be extracted."
        )
#                DOCUMENT HASHING
def generate_document_id(file_path: str) -> str:
    """
    Generates unique document ids.
    """
    with open(file_path, "rb") as file:
        content = file.read()
    return hashlib.md5(content).hexdigest()
#                 DOCUMENT LOADERS
def load_pdf(file_path: str) -> List[Document]:
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
    except Exception as e:
        raise CorruptedDocumentError(
            f"Unable to process PDF : {e}"
        )
def load_txt(file_path: str) -> List[Document]:
    try:
        loader = TextLoader(
            file_path=file_path,
            encoding="utf-8"
        )
        documents = loader.load()
        return documents
    except Exception as e:
        raise CorruptedDocumentError(
            f"Unable to process TXT : {e}"
        )
def load_docx(file_path: str) -> List[Document]:
    try:
        loader = Docx2txtLoader(file_path)
        documents = loader.load()
        return documents
    except Exception as e:
        raise CorruptedDocumentError(
            f"Unable to process DOCX : {e}"
        )
#               METADATA EXTRACTION
def add_metadata(
        documents: List[Document],
        file_path: str
) -> List[Document]:
    """
    Adds metadata required by
    downstream components.
    """
    filename = os.path.basename(file_path)
    document_id = generate_document_id(
        file_path
    )
    total_pages = len(documents)
    for index, document in enumerate(documents):
        document.metadata["source"] = filename
        document.metadata["document_id"] = document_id
        document.metadata["total_pages"] = total_pages
        document.metadata["page"] = (
            document.metadata.get(
                "page",
                index
            ) + 1

        )
    return documents
#              DOCUMENT STATISTICS
def get_document_statistics(
        documents: List[Document]
) -> Dict:
    """
    Returns useful statistics
    for analytics dashboard.
    """
    total_characters = sum(
        len(document.page_content)
        for document in documents
    )
    return {
        "total_pages": len(documents),
        "total_characters":
        total_characters,
        "average_page_length":
        round(
            total_characters /
            max(1, len(documents)),
            2
        )
    }
#                ROUTER FUNCTION
def load_document(
        file_path: str
) -> List[Document]:
    """
    Routes documents to the
    appropriate loader.
    """
    validate_document(file_path)
    extension = file_path.split(
        "."
    )[-1].lower()
    if extension == "pdf":
        documents = load_pdf(
            file_path
        )
    elif extension == "txt":
        documents = load_txt(
            file_path
        )
    elif extension == "docx":
        documents = load_docx(
            file_path
        )
    else:
        raise UnsupportedFileError(
            "Unsupported File Type."
        )
    validate_content(
        documents
    )
    documents = add_metadata(
        documents,
        file_path
    )
    return documents

    """
Future Improvements
OCR Support
CSV Support
Markdown Support
PPT Support
Image based PDFs
Batch Processing
Cloud Storage Integration
    """