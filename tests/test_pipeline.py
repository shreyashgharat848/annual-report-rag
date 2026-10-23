"""Fast tests that run without downloading models or calling the Gemini API.

Run:  pytest -q
"""

import json
from pathlib import Path

from langchain_core.language_models.fake_chat_models import FakeListChatModel

from src import config
from src.ingest import chunk_documents, load_pdf
from src.rag import RAGAnswer, RAGPipeline

PDF = config.PDF_PATH


def test_pdf_has_expected_pages():
    pages = load_pdf(PDF)
    assert 25 <= len(pages) <= 30
    assert pages[0].metadata["page_number"] == 1
    assert pages[-1].metadata["page_number"] == len(pages)


def test_running_footer_is_removed():
    pages = load_pdf(PDF)
    assert not any("Annual Report 2025-26 Page" in p.page_content for p in pages[1:])


def test_chunks_keep_page_numbers():
    chunks = chunk_documents(load_pdf(PDF), chunk_size=500, chunk_overlap=75)
    assert all(len(c.page_content) <= 500 for c in chunks)
    assert all(isinstance(c.metadata["page_number"], int) for c in chunks)
    assert len({c.metadata["chunk_id"] for c in chunks}) == len(chunks)


def test_eval_answers_exist_on_expected_pages():
    """Guards the test set: each expected keyword really appears on at least one expected page."""
    text = {p.metadata["page_number"]: " ".join(p.page_content.lower().split()) for p in load_pdf(PDF)}
    for q in json.loads(Path("eval/questions.json").read_text()):
        for group in q["expected_keywords"]:
            assert any(v.lower() in text[pg] for pg in q["expected_pages"] for v in group), (q["id"], group)


class _FakeStore:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search_with_relevance_scores(self, question, k=4):
        return [(d, 0.9) for d in self.docs[:k]]


def test_pipeline_formats_citations_and_refusals():
    chunks = chunk_documents(load_pdf(PDF), 800, 120)
    llm = FakeListChatModel(responses=["Revenue was Rs. 4,820 crore [Page 3].", config.NOT_FOUND_MESSAGE])
    pipe = RAGPipeline(_FakeStore(chunks), llm=llm, top_k=3)

    first = pipe.ask("What was revenue?")
    assert first.cited_pages == [3] and not first.is_not_found and len(first.sources) == 3

    second = pipe.ask("What is the CEO's favourite colour?")
    assert second.is_not_found


def test_cited_pages_parsing():
    a = RAGAnswer("q", "A [Page 4] and B [page 12], again [Page 4].")
    assert a.cited_pages == [4, 12]
