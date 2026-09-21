import logfire
import time
from app.agents.state import AgentState
from app.services.retrieval.qdrant_service import search_enterprise_knowledge
from app.services.retrieval.ranking_service import rerank_document_records

def retrieve_node(state: AgentState):
    """
    Performs vector search and semantic reranking for technical queries.
    """
    query = state["current_query"]
    
    
    # Standard Retrieval Logic
    with logfire.span(" Knowledge Retrieval"):
        logfire.info(f"Searching Qdrant for: {query}")
        vector_start = time.perf_counter()
        raw_results = search_enterprise_knowledge(query, limit=15)
        vector_duration_ms = int((time.perf_counter() - vector_start) * 1000)
        logfire.info(f"Retrieved {len(raw_results)} candidates from Vector DB")

        with logfire.span("Semantic Reranking"):
            rerank_start = time.perf_counter()
            reranked_docs = rerank_document_records(query, raw_results, top_n=5)
            rerank_duration_ms = int((time.perf_counter() - rerank_start) * 1000)
            logfire.info("Reranking complete. Kept top 5 most relevant chunks.")
    
    return {
        "documents": reranked_docs,
        "status": f"Found technical context.",
        "plan": state["plan"] + ["Context Retrieved"],
        "execution_steps": [
            {"stage": "Vector Search", "status": "success", "duration_ms": vector_duration_ms},
            {"stage": "Reranker", "status": "success", "duration_ms": rerank_duration_ms},
        ],
    }
