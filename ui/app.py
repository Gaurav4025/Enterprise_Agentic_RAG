"""
IntelliRAG — Minimalist Monochrome Interface
Enterprise Agentic RAG System
"""

import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kubernetes AI Helpdesk",
    page_icon="▪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium Monochrome Styling ────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Reset */
    html, body, [class*="css"], .stMarkdown, p, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }

    /* Core Canvas */
    .stApp {
        background-color: #09090b;
        color: #e4e4e7;
    }

    /* Sidebar Aesthetic */
    [data-testid="stSidebar"] {
        background-color: #0d0d10 !important;
        border-right: 1px solid #1f1f23 !important;
    }

    [data-testid="stSidebar"] * {
        color: #a1a1aa;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        color: #f4f4f5 !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }

    /* Brand Header in Sidebar */
    .brand-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff !important;
        letter-spacing: -0.02em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .brand-subtitle {
        font-size: 0.75rem;
        color: #71717a !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 2px;
        margin-bottom: 12px;
    }

    /* Chat Messages */
    .chat-row-user {
        display: flex;
        justify-content: flex-end;
        margin: 14px 0 6px 0;
    }

    .chat-row-assistant {
        display: flex;
        justify-content: flex-start;
        margin: 14px 0 6px 0;
    }

    .user-bubble {
        background: #27272a;
        color: #f4f4f5;
        border: 1px solid #3f3f46;
        padding: 14px 18px;
        border-radius: 14px 14px 2px 14px;
        max-width: 82%;
        font-size: 0.92rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .assistant-bubble {
        background: #121215;
        color: #e4e4e7;
        border: 1px solid #27272a;
        padding: 18px 22px;
        border-radius: 14px 14px 14px 2px;
        max-width: 90%;
        font-size: 0.92rem;
        line-height: 1.65;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }

    .message-meta {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #71717a;
        margin-bottom: 6px;
        font-weight: 500;
    }

    /* Minimal Monochrome Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #18181b;
        color: #d4d4d8;
        border: 1px solid #27272a;
        border-radius: 6px;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.01em;
        margin-bottom: 12px;
    }

    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #22c55e;
    }

    .status-dot-cache {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #e4e4e7;
        box-shadow: 0 0 6px #ffffff;
    }

    /* Metric Cards */
    [data-testid="metric-container"] {
        background: #131316 !important;
        border: 1px solid #222226 !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
    }

    [data-testid="metric-container"] label {
        color: #71717a !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f4f4f5 !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }

    /* Minimalist Accordions & Expanders */
    div[data-testid="stExpander"] {
        background: #111114 !important;
        border: 1px solid #222226 !important;
        border-radius: 8px !important;
        margin-top: 10px !important;
    }

    div[data-testid="stExpander"] details summary {
        color: #a1a1aa !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 8px 14px !important;
    }

    div[data-testid="stExpander"] details summary:hover {
        color: #f4f4f5 !important;
    }

    /* Thought Process / Plan Steps */
    .thought-step {
        background: #18181b;
        border-left: 2px solid #52525b;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 0 6px 6px 0;
        font-size: 0.8rem;
        color: #d4d4d8;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Source Cards */
    .source-box {
        background: #151518;
        border: 1px solid #26262b;
        border-radius: 6px;
        padding: 10px 12px;
        margin: 6px 0;
    }

    .source-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #a1a1aa;
        background: #202024;
        border: 1px solid #2e2e34;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
        margin-bottom: 6px;
    }

    /* Chat Input Bar */
    .stChatInputContainer, [data-testid="stChatInput"] {
        border-color: #27272a !important;
    }

    .stChatInput textarea {
        background: #121215 !important;
        border: 1px solid #27272a !important;
        color: #f4f4f5 !important;
        border-radius: 10px !important;
        font-size: 0.92rem !important;
    }

    .stChatInput textarea:focus {
        border-color: #52525b !important;
        box-shadow: 0 0 0 1px #52525b !important;
    }

    /* Buttons */
    .stButton button {
        background: #161619 !important;
        color: #d4d4d8 !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.84rem !important;
        transition: all 0.15s ease-in-out !important;
    }

    .stButton button:hover {
        background: #222226 !important;
        color: #ffffff !important;
        border-color: #3f3f46 !important;
    }

    /* Dividers */
    hr {
        border-color: #1f1f23 !important;
        margin: 16px 0 !important;
    }

    /* Code Blocks */
    code, pre {
        background: #141417 !important;
        border: 1px solid #242429 !important;
        color: #e4e4e7 !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    ::-webkit-scrollbar-track {
        background: #09090b;
    }
    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46;
    }
</style>
""", unsafe_allow_html=True)


# ── Session State Initialization ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "cache_hits" not in st.session_state:
    st.session_state.cache_hits = 0


# ── Sidebar Navigation & Status ───────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="brand-title">INTELLI·RAG</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">Kubernetes AI Helpdesk</p>', unsafe_allow_html=True)
    st.divider()

    # Session Management
    st.markdown("#### Session")
    st.caption("Active Thread")
    st.code(st.session_state.thread_id[:16] + "…", language=None)

    if st.button("New Session", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.session_state.cache_hits = 0
        st.rerun()

    st.divider()

    # Telemetry & Metrics
    st.markdown("#### Telemetry")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.total_queries)
    with col2:
        st.metric("Cache Hits", st.session_state.cache_hits)




# ── Chat Messages Container ───────────────────────────────────────────────────
chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align:center; padding: 70px 20px; color:#52525b;">
            <p style="font-size: 0.95rem; color:#f4f4f5; margin-bottom: 6px; font-weight: 500;">
                Kubernetes Operations & Support Helpdesk
            </p>
            <p style="font-size: 0.82rem; color:#71717a; max-width: 500px; margin: 0 auto 24px auto;">
                Ask technical questions about your Kubernetes clusters, pod autoscaling, ingress, SR-IOV networking, or cluster operations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-row-user">
                    <div class="user-bubble">
                        <div class="message-meta">User</div>
                        {msg["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                meta = msg.get("meta", {})
                status = meta.get("status", "")
                thought_process = meta.get("thought_process", [])
                sources = meta.get("sources", [])

                dot_class = "status-dot-cache" if ("Cache hit" in status or "⚡" in status) else "status-dot"

                st.markdown(f"""
                <div class="chat-row-assistant">
                    <div class="assistant-bubble">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <div class="message-meta">Kubernetes Helpdesk</div>
                            {f'<div class="status-badge"><span class="{dot_class}"></span> {status}</div>' if status else ''}
                        </div>
                        <div>{msg["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Monochromatic expandable reasoning details
                if thought_process or sources:
                    col_exp1, col_exp2 = st.columns([1, 1])
                    if thought_process:
                        with col_exp1:
                            with st.expander("Execution Steps", expanded=False):
                                for step in thought_process:
                                    st.markdown(f'<div class="thought-step">{step}</div>', unsafe_allow_html=True)

                    if sources:
                        with col_exp2:
                            with st.expander(f"Retrieved Evidence ({len(sources)} sources)", expanded=False):
                                for i, src in enumerate(sources[:4], 1):
                                    text = src.replace("CONTENT: ", "").strip()
                                    st.markdown(f"""
                                    <div class="source-box">
                                        <span class="source-tag">Source Chunk #{i}</span>
                                        <p style="color:#a1a1aa; font-size:0.78rem; margin:4px 0 0 0; line-height:1.45;">
                                            {text[:320]}{"…" if len(text) > 320 else ""}
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)


# ── Quick Suggestions (only if history is empty) ──────────────────────────────
if not st.session_state.messages:
    st.markdown('<p style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em; color:#71717a; margin-bottom:10px;">Common Kubernetes Inquiries</p>', unsafe_allow_html=True)
    suggestions = [
        "Explain SR-IOV and its benefits in Kubernetes networking",
        "What is Kubernetes horizontal pod autoscaling?",
        "How do cron jobs function in enterprise Kubernetes?",
        "Explain the routing mechanism between pods and physical NICs",
    ]
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state._pending_input = suggestion
            st.rerun()


# ── Chat Input Processing ─────────────────────────────────────────────────────
user_input = st.chat_input("Ask any Kubernetes, networking, or infrastructure question…")

if hasattr(st.session_state, "_pending_input"):
    user_input = st.session_state._pending_input
    del st.session_state._pending_input

if user_input and user_input.strip():
    cleaned_input = user_input.strip()

    # Append user entry
    st.session_state.messages.append({"role": "user", "content": cleaned_input})
    st.session_state.total_queries += 1

    # Query Backend API
    with st.spinner("Consulting Kubernetes documentation…"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"q": cleaned_input, "thread_id": st.session_state.thread_id},
                timeout=120,
            )
            data = response.json()

            answer = data.get("answer", "No response received.")
            thought_process = data.get("thought_process", [])
            status = data.get("status", "")
            sources = data.get("sources", [])

            if "Cache hit" in status or "⚡" in status:
                st.session_state.cache_hits += 1

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "meta": {
                    "thought_process": thought_process,
                    "status": status,
                    "sources": sources,
                }
            })

        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Unable to connect to the backend server. Please verify the FastAPI service is running on port 8000.",
                "meta": {"status": "Connection Error"}
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Execution error: {str(e)}",
                "meta": {"status": "Error"}
            })

    st.rerun()
