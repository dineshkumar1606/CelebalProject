import time
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_classic.chains import create_history_aware_retriever
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import TOP_K, INITIAL_K, ENABLE_HISTORY, ENABLE_MULTI_QUERY
# BASE RETRIEVER
def get_base_retriever(vector_store, k: int = INITIAL_K):
    """Creates similarity based retriever."""
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
# MULTI QUERY RETRIEVER
def get_multi_query_retriever(retriever, llm):
    """Creates Multi Query Retriever."""
    try:
        return MultiQueryRetriever.from_llm(retriever=retriever, llm=llm)
    except Exception:
        return retriever
# HISTORY AWARE RETRIEVER
def get_history_aware_retriever(retriever, llm):
    """Creates history aware retriever."""
    try:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Given the chat history and latest user question, generate an independent question."
            ),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        return create_history_aware_retriever(llm, retriever, prompt)
    except Exception:
        return retriever
# ADVANCED RETRIEVER
def get_advanced_retriever(vector_store, llm):
    """Main entry point for retrieval layer."""
    retriever = get_base_retriever(vector_store)

    if ENABLE_MULTI_QUERY:
        retriever = get_multi_query_retriever(retriever, llm)

    if ENABLE_HISTORY:
        retriever = get_history_aware_retriever(retriever, llm)

    return retriever
# DOCUMENT RETRIEVAL
def retrieve_documents(retriever, question: str, chat_history=None) -> List[Document]:
    """Retrieves relevant documents."""
    try:
        documents = retriever.invoke({
            "input": question,
            "chat_history": chat_history or []
        })
        return documents
    except Exception:
        return []
# RETRIEVAL ANALYTICS
def get_retrieval_statistics(question: str, documents: List[Document], latency: float) -> Dict:
    """Analytics required by Streamlit dashboard."""
    sources = set()
    for document in documents:
        source = document.metadata.get("source", "Unknown")
        sources.add(source)

    return {
        "question": question,
        "documents": len(documents),
        "sources": len(sources),
        "latency_ms": round(latency * 1000, 2)
    }
# COMPLETE RETRIEVAL
def retrieve_context(retriever, question: str, chat_history=None):
    """Complete retrieval pipeline."""
    start_time = time.time()
    documents = retrieve_documents(retriever, question, chat_history)
    latency = time.time() - start_time
    statistics = get_retrieval_statistics(question, documents, latency)
    return {
        "documents": documents,
        "analytics": statistics
    }
