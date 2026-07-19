import time
from typing import Dict
from langchain_groq import ChatGroq
from config import LLM_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS

# INITIALIZATION
def get_llm():
    """Initializes Groq."""
    try:
        llm = ChatGroq(
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_OUTPUT_TOKENS
        )
        return llm
    except Exception as error:
        raise RuntimeError(f"Unable to initialize LLM : {error}")

# PROMPT VALIDATION
def validate_prompt(prompt: str) -> bool:
    """Validates generated prompts."""
    if not prompt or len(prompt.strip()) == 0:
        return False
    return True

# RESPONSE VALIDATION
def validate_response(response: str) -> bool:
    """Performs basic response validation."""
    if not response or len(response.strip()) == 0:
        return False
    return True

# RESPONSE GENERATION
def generate_response(prompt: str) -> str:
    """Generates grounded responses."""
    if not validate_prompt(prompt):
        raise ValueError("Invalid Prompt.")

    llm = get_llm()
    try:
        response = llm.invoke(prompt)
        output = response.content

        if not validate_response(output):
            raise RuntimeError("Invalid response generated.")

        return output
    except Exception as error:
        raise RuntimeError(f"Response Generation Failed : {error}")

# LATENCY TRACKING
def generate_response_with_metrics(prompt: str) -> Dict:
    """Generates responses along with analytics."""
    start_time = time.time()
    llm = get_llm()
    response = generate_response(prompt)
    latency = time.time() - start_time
    statistics = get_response_statistics(response, latency)

    return {
        "response": response,
        "llm": llm,
        "analytics": statistics
    }

# RESPONSE ANALYTICS
def get_response_statistics(response: str, latency: float) -> Dict:
    """Returns response analytics."""
    return {
        "characters": len(response),
        "response_time": round(latency, 2),
        "model": LLM_MODEL,
        "temperature": TEMPERATURE
    }

# FAILURE RESPONSE
def get_failure_response():
    """Graceful failure handling."""
    return """
I apologize, but I was unable to generate a response at this time.
Please try again or rephrase your question.
"""

# DEBUG SUPPORT
def test_llm_connection() -> bool:
    """Tests LLM connectivity."""
    try:
        generate_response("Hello")
        return True
    except Exception:
        return False
