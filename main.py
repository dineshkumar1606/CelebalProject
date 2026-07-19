"""
--------------------------------------------------
Smart Research Assistant
Integration Testing Layer
--------------------------------------------------
"""
import os
from dotenv import load_dotenv

from core.vector_store import get_vector_store, reset_collection
from core.ingestion import process_documents
from core.retriever import get_advanced_retriever
from core.llm import get_llm
from core.pipeline import ask_question
# ENVIRONMENT CHECK
def check_environment():
    """Checks whether API Keys are present."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")
        
    print("API Key Loaded Successfully")
# DOCUMENT INGESTION TEST
def test_ingestion():
    """Tests document processing."""
    print("\n" + "="*50 + "\nDOCUMENT INGESTION TEST\n" + "="*50)
    
    file_paths = ["uploads/cnn.pdf"]  # Add your test pdfs here
    report = process_documents(file_paths)
    
    print(report)
    return report
# RETRIEVER TEST
def test_retriever():
    """Tests retriever creation."""
    print("\n" + "="*50 + "\nRETRIEVER TEST\n" + "="*50)
    
    vector_store = get_vector_store()
    llm = get_llm()
    retriever = get_advanced_retriever(vector_store, llm)
    
    print("Retriever Created Successfully")
    return retriever
# QUESTION ANSWERING TEST
def test_pipeline(retriever):
    """Tests complete pipeline."""
    print("\n" + "="*50 + "\nPIPELINE TEST\n" + "="*50)
    question = input("\nEnter Question : ")
    report = ask_question(question, retriever)

    print("\n" + "="*50 + "\nFINAL RESPONSE\n" + "="*50)
    print(report["response"])

    print("\n" + "="*50 + "\nSTATUS\n" + "="*50)
    print(report["status"])

    if "confidence" in report:
        print("\n", report["confidence"])

    return report
# MAIN
def main():
    """Complete Integration Test."""
    try:
        check_environment()
        choice = input("\nReset Collection?\n1.Yes\n2.No\nEnter Choice : ")
        if choice == "1" or choice.lower()=="yes":
            print("Collection Reset Successfully")
            reset_collection()

        test_ingestion()
        retriever = test_retriever()
        test_pipeline(retriever)
        
        print("\n" + "="*50 + "\nPROJECT WORKING\n" + "="*50)
    except Exception as error:
        print("\n" + "="*50 + "\nERROR OCCURRED\n" + "="*50)
        print(error)
if __name__ == "__main__":
    main()
