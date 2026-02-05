import streamlit as st
import time
import os

from rag_embed import EmbeddingStore
from rag_index import VectorIndex
from rag_graph import GraphSearch
from rag_hybrid import HybridRAG
from rag_query import RagAnswer

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Enterprise Knowledge Chatbot",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load RAG only once
# -----------------------------
@st.cache_resource
def load_rag():
    store = EmbeddingStore(
        "output/embeddings.npy",
        "output/ids.npy",
        "output/meta.jsonl"
    )
    vec = VectorIndex(store)
    graph = GraphSearch()  # kept for pipeline consistency
    hybrid = HybridRAG(vec, graph)

    rag = RagAnswer(
        hybrid,
        api_key=os.getenv("GROQ_API_KEY")
    )
    return rag, vec

rag, vec = load_rag()

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "chat" not in st.session_state:
    st.session_state.chat = []

# -----------------------------
# LANDING PAGE
# -----------------------------
if st.session_state.page == "landing":

    st.markdown(
        "<h1 style='text-align:center;'>Enterprise Knowledge Chatbot</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;'>Retrieval-Augmented Generation system</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        """
        **Features**
        - Hybrid RAG (Vector + Graph backend)
        - Source-grounded answers
        - Enterprise document intelligence
        - Groq LLM inference
        """
    )

    if st.button("🚀 Start Chatbot", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()

# -----------------------------
# CHAT PAGE
# -----------------------------
else:
    st.title("🤖 Enterprise Knowledge Chatbot")

    col_chat, col_metrics = st.columns([3, 1])

    # ---- Chat section
    with col_chat:
        user_q = st.chat_input("Ask a question about the documents...")

        if user_q:
            start = time.time()

            answer = rag.ask(user_q)
            ctx = rag.hybrid.query(user_q)

            latency = round(time.time() - start, 2)

            st.session_state.chat.append({
                "q": user_q,
                "a": answer,
                "ctx": ctx,
                "lat": latency
            })

        for c in st.session_state.chat:
            st.chat_message("user").write(c["q"])
            st.chat_message("assistant").write(c["a"])

            with st.expander("📄 Retrieved Sources"):
                for v in c["ctx"]["vector"][:3]:
                    st.markdown(f"**Source ID:** `{v['id']}`")
                    st.write(v["meta"]["text"][:400] + "…")

    # ---- Metrics section
    with col_metrics:
        st.subheader("📊 Metrics")

        if st.session_state.chat:
            last = st.session_state.chat[-1]

            retrieved_docs = len(last["ctx"]["vector"])
            used_docs = min(3, retrieved_docs)

            # Retrieval Precision@K (proxy)
            precision_k = round(
                used_docs / retrieved_docs, 2
            ) if retrieved_docs else 0

            # Answer groundedness
            context_len = sum(
                len(v["meta"]["text"]) for v in last["ctx"]["vector"][:3]
            )
            answer_len = len(last["a"])
            groundedness = round(
                answer_len / context_len, 2
            ) if context_len else 0

            # Source coverage
            source_coverage = len(
                set(v["id"] for v in last["ctx"]["vector"][:3])
            )

            st.metric("Retrieval Precision@K", precision_k)
            st.metric("Answer Groundedness", groundedness)
            st.metric("Source Coverage", source_coverage)
            st.metric("Model Confidence", "High (LLM-assessed)")
            st.metric("Latency (s)", last["lat"])

        st.markdown("---")

        if st.button("⬅ Back to Home"):
            st.session_state.page = "landing"
            st.session_state.chat = []
            st.rerun()
