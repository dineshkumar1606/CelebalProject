"""
Conversation Memory Management
"""

# SAVE CONVERSATION
def save_conversation(history: list, question: str, response: str, confidence: float, status: str):
    """Appends a unified interaction record into the history array."""
    history.append({
        "question": question,
        "response": response,
        "confidence": confidence,
        "status": status
    })
    return history

# GET HISTORY
def get_history(history: list):
    """Returns the full collection of recorded logs."""
    return history

# RECENT HISTORY
def get_recent_history(history: list, limit: int = 5):
    """Extracts the latest conversational slice for context windows."""
    return history[-limit:]

# CLEAR HISTORY
def clear_history():
    """Flushes state and yields a fresh session array."""
    return []

# TOTAL QUESTIONS
def total_questions(history: list):
    """Calculates total query count processed during this session runtime."""
    return len(history)
# CHAT MESSAGES FOR THE RETRIEVER
def get_chat_messages(history: list, limit: int = 6):
    """
    Converts stored Q&A records into LangChain message objects.
    Separate from get_recent_history() - that one keeps the dict shape
    your sidebar UI displays; the retriever needs actual message objects.
    """
    from langchain_core.messages import HumanMessage, AIMessage
    messages = []
    for item in history[-limit:]:
        messages.append(HumanMessage(content=item["question"]))
        messages.append(AIMessage(content=item["response"]))
    return messages