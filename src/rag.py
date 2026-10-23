"""Step 3 of the pipeline: retrieve the top-k chunks and ask Gemini to answer using only those chunks."""

import re
import time
from dataclasses import dataclass, field

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src import config


SYSTEM_PROMPT = """You are a financial analyst assistant that answers questions about a company annual report.

Rules:

1. Answer ONLY from the context excerpts below. Do not use outside knowledge.

2. After every fact, cite the page it came from in the form [Page N].

3. Quote numbers exactly as they appear, including units (for example Rs. crore, %, EUR million).

4. If the context does not contain the answer, reply with exactly:
"{not_found}"

Do not guess and do not answer from general knowledge.

5. Keep the answer short and direct (1-4 sentences or a short bullet list).

Context excerpts:

{context}
"""


PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "Question: {question}"),
    ]
)


@dataclass
class RAGAnswer:
    question: str
    answer: str
    sources: list[Document] = field(default_factory=list)
    scores: list[float] = field(default_factory=list)

    @property
    def cited_pages(self) -> list[int]:
        """Page numbers the model cited in its answer."""
        return sorted(
            {
                int(n)
                for n in re.findall(
                    r"\[Page\s*(\d+)\]",
                    self.answer,
                    flags=re.IGNORECASE,
                )
            }
        )

    @property
    def retrieved_pages(self) -> list[int]:
        return sorted(
            {d.metadata["page_number"] for d in self.sources}
        )

    @property
    def is_not_found(self) -> bool:
        return (
            config.NOT_FOUND_MESSAGE.lower().rstrip(".")
            in self.answer.lower()
        )


def format_context(docs: list[Document]) -> str:
    return "\n\n".join(
        f"[Page {d.metadata['page_number']}]\n{d.page_content}"
        for d in docs
    )


def get_llm(api_key: str | None = None, model: str | None = None):
    from langchain_google_genai import ChatGoogleGenerativeAI

    key = api_key or config.GOOGLE_API_KEY

    if not key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. Add it to your .env file."
        )

    return ChatGoogleGenerativeAI(
        model=model or config.GEMINI_MODEL,
        temperature=1.0,
        thinking_level="low",
        max_output_tokens=300,
        max_retries=2,
        google_api_key=key,
    )


class RAGPipeline:

    def __init__(
        self,
        vectorstore: Chroma,
        llm=None,
        top_k: int = config.TOP_K,
    ):
        self.vectorstore = vectorstore
        self.llm = llm
        self.top_k = top_k

    def retrieve(
        self,
        question: str,
        k: int | None = None,
    ) -> list[tuple[Document, float]]:
        """Return (chunk, relevance score in 0..1) pairs, best first."""

        return self.vectorstore.similarity_search_with_relevance_scores(
            question,
            k=k or self.top_k,
        )

    def ask(
        self,
        question: str,
        k: int | None = None,
    ) -> RAGAnswer:

        if self.llm is None:
            print("Creating Gemini model...")
            self.llm = get_llm()

        # Measure retrieval time
        start = time.time()

        hits = self.retrieve(question, k)

        retrieval_time = time.time() - start

        print(f"RETRIEVAL TIME: {retrieval_time:.2f} seconds")

        docs = [doc for doc, _ in hits]

        # Build RAG chain
        chain = PROMPT | self.llm | StrOutputParser()

        # Measure Gemini response time
        start = time.time()

        answer = chain.invoke(
            {
                "context": format_context(docs),
                "question": question,
                "not_found": config.NOT_FOUND_MESSAGE,
            }
        ).strip()

        gemini_time = time.time() - start

        print(f"GEMINI TIME: {gemini_time:.2f} seconds")

        return RAGAnswer(
            question=question,
            answer=answer,
            sources=docs,
            scores=[score for _, score in hits],
        )