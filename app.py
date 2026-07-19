import os
import streamlit as st
from dotenv import load_dotenv

# Environment Setup
load_dotenv()

# Internal Module Layer Mapping
from config import APP_NAME, APP_VERSION, LLM_MODEL, EMBEDDING_MODEL, COLLECTION_NAME
from core.ingestion import process_documents, get_ingestion_statistics
from core.vector_store import get_collection_statistics, get_vector_store, reset_collection
from core.llm import get_llm
from core.retriever import get_advanced_retriever
from core.pipeline import ask_question
from core.memory import save_conversation, clear_history, get_recent_history, get_history, total_questions, get_chat_messages

# STREAMLIT CONFIG
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="wide"
)

# SESSION STATES
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_report" not in st.session_state:
    st.session_state.last_report = None

# INITIALIZATION
@st.cache_resource
def initialize_components():
    vector_store = get_vector_store()
    llm = get_llm()
    retriever = get_advanced_retriever(vector_store, llm)
    return vector_store, llm, retriever

vector_store, llm, retriever = initialize_components()

# HEADER
st.title("CT_CSI_DS_608 Final Project")
st.title("Smart Research Assistant")
st.caption(f"Version {APP_VERSION} | Advanced Retrieval Augmented Generation Research Platform")
st.success("Knowledge Base Active")
st.info("Advanced RAG Pipeline Active")
st.info("Upload your documents in controls section")

# SIDEBAR
with st.sidebar:
    st.header("Knowledge Base")
    try:
        statistics = get_collection_statistics()
        st.metric("Total Chunks", statistics["total_chunks"])
        st.write(f"Collection : {statistics['collection_name']}")
        st.write(f"Embedding : {statistics['embedding_model']}")
    except Exception:
        st.warning("Knowledge Base Not Initialized.")
    st.divider()
    st.header("Controls")
    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "txt", "docx"], accept_multiple_files=True)
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = clear_history()
        st.success("Chat History Cleared Successfully.")
        
    if st.button("Reset Knowledge Base"):
        try:
            reset_collection()
            initialize_components.clear()
            st.session_state.chat_history = []
            st.session_state.last_report = None
            st.success("Knowledge Base Reset Successfully.")
            st.rerun()
        except Exception as error:
            st.error(error)
            
    st.divider()
    st.header("Recent Conversations")
    history = get_recent_history(st.session_state.chat_history)

    if not history:
        st.caption("No conversations yet.")
    else:
        for item in reversed(history):
            st.write(f"**{item['status']}**")
            st.caption(item["question"])
            st.divider()
            
    st.header("Project Stack")
    st.write("• Gemini/Groq")
    st.write("• LangChain")
    st.write("• ChromaDB")
    st.write("• MiniLM")
    st.write("• RAGAS")
    st.write("• Streamlit")

# DOCUMENT INGESTION
if uploaded_files:
    with st.spinner("Processing Documents..."):
        os.makedirs("uploads", exist_ok=True)
        file_paths = []
        for file in uploaded_files:
            file_path = os.path.join("uploads", file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            file_paths.append(file_path)
            
        report = process_documents(file_paths)
        statistics = get_ingestion_statistics(report)
        st.success("Documents Indexed Successfully.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Pages", statistics["documents"])
        with col2:
            st.metric("Chunks", statistics["chunks"])
        with col3:
            st.metric("Failed", statistics["failed"])

# MAIN TABS
tab1, tab2, tab3 = st.tabs(["Research Assistant", "Evaluation Dashboard", "System Analytics"])

# TAB - 1
with tab1:
    st.subheader("Ask Questions")
    question = st.text_area("Enter your Question")

    if st.button("Generate Response", type="primary"):
        if question.strip():
            with st.spinner("Generating Response..."):
                report = ask_question(question, retriever, get_chat_messages(st.session_state.chat_history))
                st.session_state.last_report = report

                save_conversation(
                    st.session_state.chat_history,
                    question,
                    report["response"],
                    report["confidence"]["confidence_score"],
                    report["status"]
                )
                st.rerun()

    if st.session_state.last_report:
        report = st.session_state.last_report
        st.divider()

        if report["status"] == "SUCCESS":
            st.success("Document Grounded Response Generated.")
        else:
            st.warning("Grounded Refusal Generated.")

        st.subheader("Response")
        st.write(report["response"])

        if "summary" in report:
            st.subheader("Summary")
            st.write(report["summary"])

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Confidence Score", f"{report['confidence']['confidence_score']}%")
        with col2:
            st.metric("Sources Used", report["sources"])

        st.metric("Status", report["status"])

# TAB - 2
with tab2:
    st.subheader("Evaluation Dashboard")

    if st.session_state.last_report:
        confidence = st.session_state.last_report["confidence"]
        ragas = st.session_state.last_report["ragas"]
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Confidence Score", f"{confidence['confidence_score']}%")
            st.metric("Confidence Level", confidence["confidence_level"])
            st.metric("RAGAS Score", round(confidence["ragas_score"], 2))

        with col2:
            st.metric("Retrieval Quality", confidence["retrieval_score"])
            st.metric("Response Quality", confidence["response_score"])
            st.metric("Source Quality", confidence["source_score"])

        st.divider()
        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Faithfulness", ragas.get("faithfulness", 0))
        with c2:
            st.metric("Answer Relevance", ragas.get("answer_relevance", 0))
        with c3:
            st.metric("Context Precision", ragas.get("context_precision", 0))

# TAB - 3
with tab3:
    st.subheader("System Analytics")
    history = get_history(st.session_state.chat_history)
    
    total = len(history)
    success = len([item for item in history if item["status"] == "SUCCESS"])
    partial = len([item for item in history if item["status"] == "PARTIAL_SUCCESS"])
    average_confidence = sum([item["confidence"] for item in history]) / total if total != 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions Asked", total)
        st.metric("Successful Queries", success)
        st.metric("Average Confidence", f"{round(average_confidence, 2)}%")

    with col2:
        st.metric("Partial Success", partial)
        try:
            statistics = get_collection_statistics()
            st.metric("Collection Size", statistics["total_chunks"])
        except Exception:
            pass

        st.metric("LLM", LLM_MODEL)
        st.metric("Embedding", "MiniLM")

# FOOTER
st.divider()
st.caption("Smart Research Assistant | Final Internship Project")
