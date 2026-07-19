"""
--------------------------------------------------
Smart Research Assistant
Pipeline Management Layer
--------------------------------------------------
"""
import time
from typing import Dict
from core.retriever import retrieve_context
from core.prompts import build_complete_prompt, has_sufficient_context, get_failure_prompt
from core.llm import generate_response_with_metrics
from evaluation.ragas_metrics import evaluate_response
from evaluation.confidence import calculate_confidence_score, calculate_source_score, calculate_response_score, calculate_retrieval_score
from evaluation.response_metrics import get_response_metrics, generate_summary

# SOURCE COUNT
def get_source_count(documents: list) -> int:
    sources = set()
    for document in documents:
        sources.add(document.metadata.get("source", "Unknown"))
    return len(sources)

# GROUNDED REFUSAL
def is_grounded_refusal(response: str) -> bool:
    response = response.lower()
    keywords = ["could not find", "not available", "uploaded documents", "insufficient", "not present"]
    return any(keyword in response for keyword in keywords)

# RAGAS SCORE
def calculate_ragas_score(ragas_metrics: Dict) -> float:
    if ragas_metrics["status"] != "SUCCESS":
        return 0

    score = (
        ragas_metrics["faithfulness"] +
        ragas_metrics["answer_relevance"] +
        ragas_metrics["context_precision"]
    ) / 3
    return round(score, 2)

# FINAL REPORT
def build_final_report(
    question: str,
    response: str,
    documents: list,
    confidence: Dict,
    ragas: Dict,
    analytics: Dict,
    status: str
) -> Dict:
    return {
        "question": question,
        "response": response,
        "documents": documents,
        "sources": get_source_count(documents),
        "confidence": confidence,
        "ragas": ragas,
        "analytics": analytics,
        "status": status
    }

# COMPLETE PIPELINE
def ask_question(question: str, retriever, chat_history=None) -> Dict:
    pipeline_start = time.time()

    # RETRIEVAL
    retrieval_results = retrieve_context(retriever, question, chat_history)
    documents = retrieval_results["documents"]
    retrieval_time = retrieval_results["analytics"]["latency_ms"] / 1000

    # NO CONTEXT FOUND
    if not has_sufficient_context(documents):
        response = get_failure_prompt()
        confidence_results = {
            "confidence_score": 35,
            "confidence_level": "LOW",
            "ragas_score": 0,
            "retrieval_score": 0,
            "source_score": 0,
            "response_score": 35
        }
        ragas_results = {
            "status": "SKIPPED",
            "faithfulness": 0,
            "answer_relevance": 0,
            "context_precision": 0
        }
        return build_final_report(
            question, response, [], confidence_results, ragas_results, {}, "PARTIAL_SUCCESS"
        )

    # PROMPT
    prompt = build_complete_prompt(question, documents)

    # LLM
    llm_results = generate_response_with_metrics(prompt)
    response = llm_results["response"]
    llm = llm_results["llm"]
    response_time = llm_results["analytics"]["response_time"]

    # RAGAS
    ragas_results = evaluate_response(question, response, documents, llm)
    ragas_score = calculate_ragas_score(ragas_results)

    # CONFIDENCE
    source_score = calculate_source_score(get_source_count(documents))
    response_score = calculate_response_score(response)
    retrieval_score = calculate_retrieval_score(len(documents))
    confidence_results = calculate_confidence_score(
        ragas_score, retrieval_score, source_score, response_score
    )

    # ANALYTICS
    metrics = get_response_metrics(
        response, get_source_count(documents), len(documents), retrieval_time, response_time
    )
    summary = generate_summary(metrics, confidence_results, ragas_results)
    metrics["pipeline_time"] = round(time.time() - pipeline_start, 2)

    # STATUS MANAGEMENT
    if is_grounded_refusal(response):
        status = "PARTIAL_SUCCESS"
    elif ragas_results["status"] == "FAILED":
        status = "PARTIAL_SUCCESS"
    else:
        status = "SUCCESS"

    # DEBUGGING
    print(f"\nDocuments Retrieved : {len(documents)}")
    print(f"Retrieval Score : {retrieval_score}")
    print(f"RAGAS Score : {ragas_score}")
    print(f"Status : {status}\n")

    # FINAL REPORT
    report = build_final_report(
        question, response, documents, confidence_results, ragas_results, metrics, status
    )
    report["summary"] = summary

    return report
