"""Step 2 of the pipeline: embed chunks with Sentence-Transformers and store them in ChromaDB."""

import shutil
from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from src import config


@lru_cache(maxsize=2)
def get_embeddings(model_name: str = config.EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    """Load the embedding model once. Runs locally on CPU, no API key needed."""
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore(
    chunks: list[Document],
    persist_dir: str | Path | None = config.CHROMA_DIR,
    collection_name: str = config.COLLECTION_NAME,
    reset: bool = True,
) -> Chroma:
    """Create a Chroma collection from chunks. Pass persist_dir=None for an in-memory store (used in evaluation)."""
    if persist_dir is not None and reset and Path(persist_dir).exists():
        shutil.rmtree(persist_dir)

    kwargs = dict(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        collection_metadata={"hnsw:space": "cosine"},
    )
    if persist_dir is not None:
        kwargs["persist_directory"] = str(persist_dir)

    store = Chroma(**kwargs)
    ids = [c.metadata["chunk_id"] for c in chunks]
    store.add_documents(chunks, ids=ids)
    return store


def load_vectorstore(
    persist_dir: str | Path = config.CHROMA_DIR, collection_name: str = config.COLLECTION_NAME
) -> Chroma:
    if not Path(persist_dir).exists():
        raise FileNotFoundError(f"No index at {persist_dir}. Run `python build_index.py` first.")
    return Chroma(
        collection_name=collection_name,
        embedding_function=get_embeddings(),
        persist_directory=str(persist_dir),
        collection_metadata={"hnsw:space": "cosine"},
    )
