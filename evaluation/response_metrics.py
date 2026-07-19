from typing import Dict
#          RESPONSE STATISTICS
def get_response_metrics(
    response: str,
    sources: int,
    documents: int,
    retrieval_time: float,
    response_time: float
) -> Dict:
    """Aggregates processing metrics and calculates total pipeline latency."""
    return {
        "response_length": len(response),
        "sources_used": sources,
        "documents_used": documents,
        "retrieval_time": round(retrieval_time, 2),
        "response_time": round(response_time, 2),
        "total_time": round(retrieval_time + response_time, 2)
    }
#            SUMMARY STATISTICS
def generate_summary(metrics: Dict, confidence: Dict, ragas: Dict) -> Dict:
    """Flattens diverse metric layers into a singular dashboard summary."""
    return {
        "confidence": confidence["confidence_score"],
        "confidence_level": confidence["confidence_level"],
        "faithfulness": ragas["faithfulness"],
        "answer_relevance": ragas["answer_relevance"],
        "context_precision": ragas["context_precision"],
        "response_time": metrics["response_time"],
        "status": ragas["status"]
    }
