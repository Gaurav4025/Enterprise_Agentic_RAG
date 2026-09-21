# Shim — qdrant_service.py imports embed_query from this module (singular spelling).
# The actual implementation lives in embeddings.py (plural).
from app.services.retrieval.embeddings import embed_query, embed_texts, get_embedding_dim

__all__ = ["embed_query", "embed_texts", "get_embedding_dim"]
