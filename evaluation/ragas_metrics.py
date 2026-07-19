import json
from typing import Dict
from config import ENABLE_RAGAS, MINIMUM_RESPONSE_LENGTH, INSUFFICIENT_CONTEXT_RESPONSE
from core.llm import get_llm
# VALIDATION
def should_evaluate_ragas(response: str, documents: list) -> bool:
    if not ENABLE_RAGAS or not documents:
        return False
    if len(response) < MINIMUM_RESPONSE_LENGTH:
        return False
    return True
# LLM JUDGE PROMPT
JUDGE_PROMPT = """
You are an expert evaluator for a Retrieval Augmented Generation system.
Evaluate the generated answer using ONLY the retrieved context.
Give scores between 0 and 100.
Metrics
-------
1. Faithfulness
- Are all the claims made in the answer supported by the context?
2. Answer Relevance
- Does the answer appropriately answer the user's question?
3. Context Precision
- Is the retrieved context relevant to the user's question?
QUESTION
--------
{question}

CONTEXT
-------
{context}

ANSWER
------
{answer}

Return ONLY valid JSON.
{{
"faithfulness":integer,
"answer_relevance":integer,
"context_precision":integer
}}
"""
# EVALUATION
def evaluate_response(question: str, response: str, documents: list, llm=None) -> Dict:
    if not should_evaluate_ragas(response, documents):
        return {
            "status": "SKIPPED",
            "faithfulness": 0,
            "answer_relevance": 0,
            "context_precision": 0
        }
    # GROUNDED REFUSAL
    if INSUFFICIENT_CONTEXT_RESPONSE in response:
        return {
            "status": "SKIPPED",
            "faithfulness": 0,
            "answer_relevance": 0,
            "context_precision": 0
        }
    try:
        if llm is None:
            llm = get_llm()
        # LIMIT CONTEXT SIZE
        context = ("\n\n".join([document.page_content for document in documents]))[:4000]
        prompt = JUDGE_PROMPT.format(question=question, context=context, answer=response)
        result = llm.invoke(prompt)
        output = result.content.replace("```json", "").replace("```", "").strip()
        scores = json.loads(output)
        return {
            "status": "SUCCESS",
            "faithfulness": round(float(scores.get("faithfulness", 0)), 2),
            "answer_relevance": round(float(scores.get("answer_relevance", 0)), 2),
            "context_precision": round(float(scores.get("context_precision", 0)), 2)
        }
    except Exception as error:
        print(f"\nRAGAS ERROR : {error}\n")
        return {
            "status": "FAILED",
            "faithfulness": 0,
            "answer_relevance": 0,
            "context_precision": 0
        }
