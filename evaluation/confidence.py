"""
--------------------------------------------------
Smart Research Assistant
Confidence Score Layer
--------------------------------------------------
"""
from typing import Dict
from config import RAGAS_WEIGHT, RETRIEVAL_WEIGHT, SOURCE_WEIGHT, RESPONSE_WEIGHT
# RESPONSE QUALITY SCORE
def calculate_response_score(response: str) -> float:
    """Calculates response quality."""
    if len(response) < 100:
        return 70
    if len(response) < 500:
        return 85
    return 95
# SOURCE CONFIDENCE
def calculate_source_score(source_count: int) -> float:
    """Calculates source reliability score."""
    if source_count == 0:
        return 0
    if source_count == 1:
        return 80
    if source_count <= 3:
        return 90
    return 95
# CONFIDENCE LEVEL
def get_confidence_level(score: float):
    """Maps raw percentage score to a threshold category."""
    if score >= 90:
        return "HIGH"
    elif score >= 75:
        return "MEDIUM"
    return "LOW"
# FINAL CONFIDENCE SCORE
def calculate_confidence_score(
    ragas_score: float,
    retrieval_score: float,
    source_score: float,
    response_score: float
) -> Dict:
    """Calculates weighted composite confidence score."""
    confidence = (
        (ragas_score * RAGAS_WEIGHT) +
        (retrieval_score * RETRIEVAL_WEIGHT) +
        (source_score * SOURCE_WEIGHT) +
        (response_score * RESPONSE_WEIGHT)
    )
    return {
        "confidence_score": round(confidence, 2),
        "confidence_level": get_confidence_level(confidence),
        "ragas_score": ragas_score,
        "retrieval_score": retrieval_score,
        "source_score": source_score,
        "response_score": response_score
    }
def calculate_retrieval_score(chunks:int,successful:bool=True):
    """
    Calculates retrieval score.
    """
    score=0
    if successful:
        score+=50
    if chunks>=5:
        score+=45
    elif chunks>=3:
        score+=35
    elif chunks>=1:
        score+=20
    return min(
        score,
        95
    )
