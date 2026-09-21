import logfire
from portkey_ai import Portkey, createHeaders, PORTKEY_GATEWAY_URL
from langchain_openai import ChatOpenAI

from app.config import settings


# Production gateway config:
#   - Fallback: primary @rag/llama-3.3-70b-versatile → @brag/llama-3.1-8b-instant on failure
#   - Cache: simple mode (semantic requires Portkey Enterprise — silently falls back on free/starter)
#   - Retry: 2 attempts on rate limit / server error before triggering the fallback target
GATEWAY_CONFIG = {
    "strategy": {"mode": "fallback"},
    "cache": {"mode": "simple"},
    "retry": {
        "attempts": 2,
        "on_status_codes": [429, 503],
    },
    "targets": [
        {"override_params": {"model": f"@{settings.GROQ_SLUG}/llama-3.3-70b-versatile"}},
        {"override_params": {"model": f"@{settings.GROQ_SLUG_2}/llama-3.1-8b-instant"}},
    ],
}

# Native Portkey client — used in responder to read x-portkey-cache-status headers
portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY or "dummy",   # graceful: 'dummy' fails at call time, not import
    config=GATEWAY_CONFIG,
)


def get_langchain_llm(feature: str = "rag") -> ChatOpenAI:
    """
    Returns a Portkey-backed ChatOpenAI — a drop-in for ChatGroq in LangChain nodes.

    Why ChatOpenAI and not ChatGroq?
      Portkey is a proxy exposing an OpenAI-compatible endpoint.
      ChatGroq is hardwired to Groq's URL and does not support routing through a proxy.
      ChatOpenAI supports base_url (→ Portkey) + default_headers (→ Portkey auth + config).
      The @rag/model-name format is Portkey-specific; Groq's client does not understand it.
      You are still using Groq models — Portkey is just the routing middleware in the middle.
    """
    return ChatOpenAI(
        api_key=settings.PORTKEY_API_KEY or "dummy",
        base_url=PORTKEY_GATEWAY_URL,
        model=f"@{settings.GROQ_SLUG}/llama-3.3-70b-versatile",
        temperature=0,
        default_headers=createHeaders(
            api_key=settings.PORTKEY_API_KEY or "dummy",
            config=GATEWAY_CONFIG,
            metadata={
                "feature": feature,
                "_user": "rag-system",
                "environment": "production",
            },
        ),
    )


def extract_cache_status(response) -> str:
    """
    Pull x-portkey-cache-status from the native Portkey client response headers.
    Tries multiple attribute paths defensively — returns 'MISS' if not found.
    """
    for attr in ("_raw_response", "_response", "_http_response"):
        raw = getattr(response, attr, None)
        if raw is not None:
            status = getattr(raw, "headers", {}).get("x-portkey-cache-status", "")
            if status:
                return status.upper()
    return "MISS"