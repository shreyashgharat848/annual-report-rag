"""Step 1 of the pipeline: load the PDF page by page and split it into chunks that keep their page number."""

import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

PAGE_NUMBER_LINE = re.compile(r"^\s*(page\s*)?\d+\s*$", re.IGNORECASE)


def _repeated_lines(pages: list[str], min_share: float = 0.5) -> set[str]:
    """Lines that appear on most pages are running headers/footers, not content."""
    counts = Counter()
    for page in pages:
        counts.update({line.strip() for line in page.splitlines() if line.strip()})
    threshold = max(2, int(len(pages) * min_share))
    return {line for line, n in counts.items() if n >= threshold}


def _clean(text: str, noise: set[str]) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [line for line in lines if line not in noise]
    # Page numbers only appear at the top or bottom of a page. Checking only the edges matters:
    # inside the page a bare number is usually a table cell (e.g. "19" patents granted).
    for _ in range(2):
        if lines and PAGE_NUMBER_LINE.match(lines[0]):
            lines.pop(0)
        if lines and PAGE_NUMBER_LINE.match(lines[-1]):
            lines.pop()
    text = "\n".join(lines)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def load_pdf(pdf_path: str | Path) -> list[Document]:
    """Return one Document per page with a 1-based `page_number` in the metadata."""
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    raw_pages = [page.extract_text() or "" for page in PdfReader(str(pdf_path)).pages]
    noise = _repeated_lines(raw_pages) if len(raw_pages) > 3 else set()

    pages = []
    for i, raw in enumerate(raw_pages, start=1):
        text = _clean(raw, noise)
        if text:  # scanned/image-only pages have no text layer and are skipped
            pages.append(Document(page_content=text, metadata={"source": pdf_path.name, "page_number": i}))
    return pages


def chunk_documents(pages: list[Document], chunk_size: int = 800, chunk_overlap: int = 120) -> list[Document]:
    """Split pages into overlapping chunks. Chunks never cross a page boundary, so every chunk has one page number."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"p{chunk.metadata['page_number']}-c{i}"
    return chunks


if __name__ == "__main__":
    from src import config

    pages = load_pdf(config.PDF_PATH)
    chunks = chunk_documents(pages, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    print(f"Pages: {len(pages)} | Chunks: {len(chunks)}")
    print(chunks[0].metadata, "\n", chunks[0].page_content[:300])
