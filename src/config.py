"""Central configuration. Values can be overridden with environment variables or a .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent

# Data
PDF_PATH = Path(os.getenv("PDF_PATH", ROOT_DIR / "data" / "veltrix_annual_report_fy2026.pdf"))
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", ROOT_DIR / "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "annual_report")

# Chunking (chosen after the chunk-size comparison in evaluate.py)
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 120))

# Retrieval
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", 4))

# Generation
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-3.6-flash"
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.0))

# The exact sentence the model must use when the answer is not in the document.
NOT_FOUND_MESSAGE = "I could not find this information in the report."
