"""
Prompt Engineering Layer
Responsibilities
----------------
1. Prompt Construction
2. Context Management
3. Hallucination Prevention
4. No Answer Strategy
5. Summary Generation
6. Source Grounding
"""
from typing import List
from langchain_core.documents import Document
from config import APP_NAME, MAX_CONTEXT_CHARACTERS
from config import (
    INSUFFICIENT_CONTEXT_RESPONSE
)
# SYSTEM PROMPT
def get_system_prompt() -> str:
    """Defines the behaviour of the Smart Research Assistant."""
    return f"""
You are {APP_NAME}.
You are an advanced AI Research Assistant designed to answer questions ONLY from the provided context.
RULES:
------
1. NEVER hallucinate.
2. Answer ONLY from the retrieved context.
3. If sufficient information is not available, explicitly state that you could not find enough information in the uploaded documents.
4. NEVER fabricate information.
5. NEVER use outside knowledge.
6. Keep responses factual, grounded and concise.
7. Provide a brief summary at the end of every answer whenever possible.
8. If multiple documents discuss the same topic, synthesize the information appropriately.
"""
# FAILURE PROMPT
def get_failure_prompt() -> str:
    """Used whenever retrieval fails."""
    return """
I couldn't find sufficient information inside the uploaded documents to answer this question.
Please upload additional documents or rephrase the query.
"""
# OUTPUT FORMAT
def get_output_prompt() -> str:
    """Defines the expected output format."""
    return """
OUTPUT FORMAT
-------------
Answer:
Provide a detailed and grounded answer.

Summary:
Provide a short summary of the response.

If information is insufficient, do not attempt to fabricate an answer.
"""
# CONTEXT BUILDER
def build_context(documents: List[Document]) -> str:
    """Creates context from retrieved documents."""
    context = ""
    current_size = 0
    for document in documents:
        source = document.metadata.get("source", "Unknown")
        page = document.metadata.get("page", "Unknown")
        chunk = document.metadata.get("chunk_number", "Unknown")
        content = f"\nSOURCE : {source}\nPAGE : {page}\nCHUNK : {chunk}\nCONTENT :\n{document.page_content}\n"
        if current_size + len(content) > MAX_CONTEXT_CHARACTERS:
            break
        context += content
        current_size += len(content)
    return context
# QUESTION PROMPT
def get_question_prompt(question: str) -> str:
    """Formats user questions."""
    return f"\nQUESTION\n{question}\n"
# COMPLETE PROMPT
def build_complete_prompt(question: str, documents: List[Document]) -> str:
    """Creates the final prompt sent to the LLM."""
    context = build_context(documents)
    return f"""
{get_system_prompt()}
RETRIEVED CONTEXT
{context}
{get_question_prompt(question)}
{get_output_prompt()}
"""
# RETRIEVAL VALIDATION
def has_sufficient_context(documents: List[Document]) -> bool:
    """Checks whether retrieved context exists."""
    if not documents:
        return False

    total_characters = sum(len(document.page_content) for document in documents)
    return total_characters > 0
# DEBUG SUPPORT
def get_context_statistics(documents: List[Document]):
    """Used by analytics dashboard."""
    total_characters = sum(len(document.page_content) for document in documents)

    return {
        "documents": len(documents),
        "characters": total_characters,
        "max_context": MAX_CONTEXT_CHARACTERS
    }
def get_failure_prompt():
    """
    Grounded refusal.
    """
    return (
        INSUFFICIENT_CONTEXT_RESPONSE
    )
