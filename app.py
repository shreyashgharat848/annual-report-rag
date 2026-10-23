"""Streamlit chat interface for the Annual Report Q&A Assistant.

Run:  streamlit run app.py
"""

import hashlib
import tempfile
import time
from pathlib import Path

import streamlit as st

from src import config
from src.ingest import chunk_documents, load_pdf
from src.rag import RAGPipeline, get_llm
from src.vectorstore import build_vectorstore, load_vectorstore

st.set_page_config(page_title="Annual Report Q&A", page_icon="📊", layout="wide")

EXAMPLE_QUESTIONS = [
    "What was the revenue from operations in FY2025-26?",
    "How much did the company pay to acquire DataHarbor Analytics?",
    "What is the revenue guidance for FY2026-27?",
    "Who is the Chief Financial Officer?",
    "What was the voluntary attrition rate?",
]


@st.cache_resource(show_spinner="Loading the index...")
def default_store():
    try:
        return load_vectorstore()
    except FileNotFoundError:
        pages = load_pdf(config.PDF_PATH)
        return build_vectorstore(chunk_documents(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP))


@st.cache_resource(show_spinner="Indexing your PDF...")
def uploaded_store(file_hash: str, data: bytes, name: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_bytes(data)
        pages = load_pdf(path)
    chunks = chunk_documents(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    return build_vectorstore(chunks, persist_dir=None, collection_name=f"upload_{file_hash[:12]}"), len(pages)


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    api_key = config.GOOGLE_API_KEY or st.text_input("Gemini API key", type="password",
                                                     help="Get a free key at https://aistudio.google.com/apikey")
    top_k = st.slider("Chunks to retrieve (top-k)", 2, 8, config.TOP_K)
    show_scores = st.checkbox("Show retrieval scores", value=True)

    st.divider()
    st.subheader("Document")
    upload = st.file_uploader("Use your own PDF (optional)", type="pdf")
    if upload:
        data = upload.getvalue()
        store, n_pages = uploaded_store(hashlib.md5(data).hexdigest(), data, upload.name)
        doc_name = upload.name
    else:
        store = default_store()
        doc_name = config.PDF_PATH.name
        n_pages = None
        with open(config.PDF_PATH, "rb") as f:
            st.download_button("Download sample report", f, file_name=doc_name, mime="application/pdf")

    st.caption(f"**{doc_name}**  \n{store._collection.count()} chunks indexed"
               + (f" from {n_pages} pages" if n_pages else ""))
    st.caption(f"Embeddings: `{config.EMBEDDING_MODEL.split('/')[-1]}`  \nLLM: `{config.GEMINI_MODEL}`")

    if st.button("Clear chat"):
        st.session_state.messages = []

# ---------------- Main ----------------
st.title("📊 Annual Report Q&A Assistant")
st.caption("Ask questions about the report. Every answer cites the page it came from, "
           "and the assistant says so when the answer is not in the document.")

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_sources(sources, scores):
    with st.expander(f"Sources ({len(sources)} excerpts)"):
        for doc, score in zip(sources, scores):
            label = f"**Page {doc.metadata['page_number']}**"
            if show_scores:
                label += f" · relevance {score:.2f}"
            st.markdown(label)
            st.text(doc.page_content[:700] + ("..." if len(doc.page_content) > 700 else ""))


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            render_sources(msg["sources"], msg["scores"])

if not st.session_state.messages:
    st.markdown("**Try one of these:**")
    cols = st.columns(len(EXAMPLE_QUESTIONS))
    for col, q in zip(cols, EXAMPLE_QUESTIONS):
        if col.button(q, use_container_width=True):
            st.session_state.pending = q
            st.rerun()

question = st.chat_input("Ask a question about the report") or st.session_state.pop("pending", None)

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not api_key:
            st.warning("Add your Gemini API key in the sidebar or in the .env file.")
            st.stop()
        with st.spinner("Searching the report..."):
            start = time.time()
            try:
                result = RAGPipeline(store, llm=get_llm(api_key), top_k=top_k).ask(question)
            except Exception as e:  # show API errors in the UI instead of crashing
                st.error(f"Something went wrong: {e}")
                st.stop()
            elapsed = time.time() - start
        st.markdown(result.answer)
        st.caption(f"Answered in {elapsed:.1f}s")
        render_sources(result.sources, result.scores)

    st.session_state.messages.append(
        {"role": "assistant", "content": result.answer, "sources": result.sources, "scores": result.scores}
    )
