import re
import logfire
from app.agents.state import AgentState
from app.config import settings
from langchain_groq import ChatGroq
from app.gateway.client import portkey_client, extract_cache_status

# Direct ChatGroq fallback instance
llm = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL, temperature=0)


def generate_node(state: AgentState):
    """
    Synthesizes a response using both Documentation Context AND Conversation History.
    Uses Portkey if configured (to detect cache hits and virtual routing),
    and gracefully falls back to direct ChatGroq if Portkey is not configured or errors.
    """
    query = state["current_query"]

    history_str = ""
    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_str += f"{role}: {msg['content']}\n"

    user_msg = state["messages"][-1]["content"] if state["messages"] else ""

    if query == "CONVERSATIONAL":
        logfire.info("Generating conversational response using memory.")
        prompt = f"""
        You are a friendly and helpful Enterprise AI Assistant.
        Answer the user's latest message using the CONVERSATION HISTORY below.

        CONVERSATION HISTORY:
        {history_str}

        LATEST MESSAGE:
        "{user_msg}"
        """
    else:
        logfire.info("Generating technical RAG response.")
        max_context_chars = 25000
        full_context = ""

        for doc in state["documents"]:
            if len(full_context) + len(doc) < max_context_chars:
                full_context += doc + "\n\n"
            else:
                logfire.warning("Context truncated to fit Groq TPM limits.")
                break

        prompt = f"""
        You are a Senior Technical Architect specializing in Kubernetes, Intel hardware, and Enterprise Networking.
        Answer the question using the TECHNICAL CONTEXT provided.

        TECHNICAL CONTEXT:
        {full_context}

        CONVERSATION HISTORY:
        {history_str}

        USER QUESTION:
        "{user_msg}"
        """

    with logfire.span(" LLM Synthesis"):
        content = None
        is_cache_hit = False

        # Attempt Portkey gateway if API key is present
        if settings.PORTKEY_API_KEY:
            try:
                response = portkey_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1
                )
                content = response.choices[0].message.content
                cache_status = extract_cache_status(response)
                is_cache_hit = (cache_status == "HIT")
            except Exception as e:
                logfire.warning(f"Portkey gateway call failed: {e}. Falling back to ChatGroq direct.")

        # Fallback to direct ChatGroq
        if not content:
            try:
                res = llm.invoke(prompt)
                content = res.content
            except Exception as e:
                logfire.error(f"LLM Generation failed: {e}")
                raise e

        # Clean think tags if model outputs internal reasoning block
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        if is_cache_hit:
            logfire.info("⚡ Gateway Cache Hit — response served from Portkey cache.")
            plan_update = state["plan"] + ["Cache: Hit ⚡"]
            status = "Cache hit — instant response."
        else:
            logfire.info(" Response synthesised via LLM.")
            plan_update = state["plan"]
            status = "Response generated."

        return {
            "final_answer": content,
            "status": status,
            "plan": plan_update,
            "messages": [{"role": "assistant", "content": content}]
        }