import logfire
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.config import settings
from app.services.retrieval.embedding import embed_query


# Initialize Qdrant Client
client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

def search_enterprise_knowledge(query: str, limit: int = 8):
    """
    Performs a high-precision search in the enterprise knowledge base.
    Uses the modern query_points interface.
    """
    try:
        query_vector = embed_query(query)

        # Using query_points - the modern standard for Qdrant
        response = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            limit=limit,
            with_payload=True # JSON
        )

        results = []
        for res in response.points:
            payload = res.payload or {}
            metadata = {k: v for k, v in payload.items() if k != "text"}
            results.append({
                "content": payload.get("text", ""),
                "source": payload.get("source", "Unknown"),
                "source_type": payload.get("source_type"),
                "score": res.score,
                "metadata": metadata,
            })
        
        return results
    except Exception as e:
        logfire.error(f"Qdrant Search Failed: {e}")
        return []
