import re
import time
from app.agents.state import AgentState
from app.config import settings
from langchain_groq import ChatGroq
import logfire

# Portkey-backed LLM: fallback + cache + retry — same .invoke() interface as ChatGroq
llm = ChatGroq(api_key = settings.GROQ_API_KEY, model = settings.GROQ_MODEL, temperature= 0)
    

def planner_node(state: AgentState):
    """
    The Planner determines if a search is needed based on the ENTIRE conversation.
    """
    # Get the conversation history (excluding the latest message)
    history = ""
    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"
    
    user_message = state["messages"][-1]["content"] if state["messages"] else ""
    
    prompt = f"""
    You are an intelligent Assistant Planner. 
    Analyze the conversation history and the latest user message.
    
    CONVERSATION HISTORY:
    {history}
    
    LATEST MESSAGE:
    "{user_message}"
    
    Task:
    1. If the latest message is a greeting (hi, hello) or a question that can be answered using ONLY the conversation history above (e.g., "what is my name"), respond with 'CONVERSATIONAL'.
    2. If it is a technical question about Kubernetes, Intel, or Networking that requires fresh documentation, output a refined search query.
    
    Output ONLY 'CONVERSATIONAL' or the search query.
    """
    
    with logfire.span(" Planner Decision"):
        start_time = time.perf_counter()
        decision_raw = llm.invoke(prompt).content
        duration_ms = int((time.perf_counter() - start_time) * 1000)
        decision = re.sub(r"<think>.*?</think>", "", decision_raw, flags=re.DOTALL).strip().strip('"\'')
        logfire.info(f"Intent identified: {decision}")
    
    if decision == "CONVERSATIONAL":
        return {
            "current_query": "CONVERSATIONAL",
            "status": "Handling conversationally (using memory)...",
            "plan": ["Intent: Conversational/Memory", "Retrieval: Skipped"],
            "execution_steps": [
                {"stage": "Planner", "status": "success", "duration_ms": duration_ms}
            ],
        }
    
    return {
        "current_query": decision,
        "status": f"Technical research needed. Searching for: {decision}",
        "plan": ["Intent: Technical", f"Search Term: {decision}"],
        "execution_steps": [
            {"stage": "Planner", "status": "success", "duration_ms": duration_ms}
        ],
    }
