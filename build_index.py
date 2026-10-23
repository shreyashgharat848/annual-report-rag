"""Build the ChromaDB index from the annual report PDF.

Usage:
    python build_index.py
    python build_index.py --pdf path/to/report.pdf --chunk-size 800 --overlap 120
"""

import argparse
import time

from src import config
from src.ingest import chunk_documents, load_pdf
from src.vectorstore import build_vectorstore


def main():
    parser = argparse.ArgumentParser(description="Index a PDF report into ChromaDB")
    parser.add_argument("--pdf", default=str(config.PDF_PATH))
    parser.add_argument("--chunk-size", type=int, default=config.CHUNK_SIZE)
    parser.add_argument("--overlap", type=int, default=config.CHUNK_OVERLAP)
    args = parser.parse_args()

    start = time.time()
    pages = load_pdf(args.pdf)
    chunks = chunk_documents(pages, args.chunk_size, args.overlap)
    print(f"Loaded {len(pages)} pages -> {len(chunks)} chunks (size={args.chunk_size}, overlap={args.overlap})")

    store = build_vectorstore(chunks)
    print(f"Indexed {store._collection.count()} chunks into {config.CHROMA_DIR} in {time.time() - start:.1f}s")


if __name__ == "__main__":
    main()
