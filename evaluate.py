"""Evaluate the RAG pipeline on the test questions in eval/questions.json.

Two evaluations:
  retrieval  Compares chunk sizes. For each size, checks whether a chunk from the correct page is in the
             top-k results (Hit@k) and how high it ranks (MRR). Runs locally, no API key needed.
  answers    Runs the full pipeline with Gemini and checks each answer: correct facts for answerable
             questions, and a refusal for questions that are not in the report. Needs GOOGLE_API_KEY.

Usage:
  python evaluate.py --mode retrieval
  python evaluate.py --mode answers
  python evaluate.py --mode all
"""

import argparse
import json
import time
from pathlib import Path

import pandas as pd

from src import config
from src.ingest import chunk_documents, load_pdf
from src.rag import RAGPipeline, get_llm
from src.vectorstore import build_vectorstore, load_vectorstore

QUESTIONS_PATH = Path("eval/questions.json")
RESULTS_DIR = Path("eval/results")


def load_questions():
    return json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))


def keywords_found(answer: str, groups: list[list[str]]) -> bool:
    """Every group must match; any variant inside a group counts."""
    a = " ".join(answer.lower().split())
    return all(any(v.lower() in a for v in group) for group in groups)


# ---------------------------------------------------------------- retrieval
def evaluate_retrieval(chunk_sizes: list[int], top_k: int) -> pd.DataFrame:
    questions = [q for q in load_questions() if q["answerable"]]
    pages = load_pdf(config.PDF_PATH)
    rows = []

    for size in chunk_sizes:
        overlap = int(size * 0.15)
        chunks = chunk_documents(pages, size, overlap)
        store = build_vectorstore(chunks, persist_dir=None, collection_name=f"eval_{size}")
        pipeline = RAGPipeline(store, top_k=top_k)

        hits, reciprocal_ranks = 0, []
        for q in questions:
            ranked_pages = [d.metadata["page_number"] for d, _ in pipeline.retrieve(q["question"])]
            rank = next((i + 1 for i, p in enumerate(ranked_pages) if p in q["expected_pages"]), None)
            hits += rank is not None
            reciprocal_ranks.append(1 / rank if rank else 0.0)

        rows.append({
            "chunk_size": size,
            "overlap": overlap,
            "num_chunks": len(chunks),
            f"hit@{top_k}": round(hits / len(questions), 3),
            "mrr": round(sum(reciprocal_ranks) / len(questions), 3),
        })
        store.delete_collection()
        print(f"chunk_size={size:>5}  chunks={len(chunks):>4}  hit@{top_k}={hits}/{len(questions)}  "
              f"mrr={rows[-1]['mrr']:.3f}")

    df = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_DIR / "chunk_size_comparison.csv", index=False)
    print("\n" + df.to_markdown(index=False))
    return df


# ---------------------------------------------------------------- answers
def evaluate_answers(top_k: int, delay: float) -> pd.DataFrame:
    questions = load_questions()
    try:
        store = load_vectorstore()
    except FileNotFoundError:
        store = build_vectorstore(chunk_documents(load_pdf(config.PDF_PATH), config.CHUNK_SIZE, config.CHUNK_OVERLAP))
    pipeline = RAGPipeline(store, llm=get_llm(), top_k=top_k)

    rows = []
    for q in questions:
        res = pipeline.ask(q["question"])
        if q["answerable"]:
            correct = keywords_found(res.answer, q["expected_keywords"]) and not res.is_not_found
            citation_ok = bool(set(res.cited_pages) & set(q["expected_pages"]))
        else:
            correct = res.is_not_found
            citation_ok = None
        rows.append({
            "id": q["id"],
            "question": q["question"],
            "answerable": q["answerable"],
            "correct": correct,
            "citation_ok": citation_ok,
            "cited_pages": res.cited_pages,
            "retrieved_pages": res.retrieved_pages,
            "answer": res.answer.replace("\n", " "),
        })
        print(f"[{'PASS' if correct else 'FAIL'}] Q{q['id']}: {q['question']}\n        -> {res.answer[:160]}")
        time.sleep(delay)  # stay within free-tier rate limits

    df = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RESULTS_DIR / "answer_eval.csv", index=False)

    ans = df[df.answerable]
    unans = df[~df.answerable]
    summary = (
        f"Overall: {int(df.correct.sum())}/{len(df)} questions handled correctly\n"
        f"Answerable: {int(ans.correct.sum())}/{len(ans)} answered correctly\n"
        f"Citations: {int(ans.citation_ok.sum())}/{len(ans)} answers cited a correct page\n"
        f"Not in report: {int(unans.correct.sum())}/{len(unans)} correctly declined\n"
    )
    (RESULTS_DIR / "summary.txt").write_text(summary, encoding="utf-8")
    print("\n" + summary)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["retrieval", "answers", "all"], default="all")
    parser.add_argument("--chunk-sizes", type=int, nargs="+", default=[300, 500, 800, 1200])
    parser.add_argument("--top-k", type=int, default=config.TOP_K)
    parser.add_argument("--delay", type=float, default=4.0, help="Seconds between Gemini calls")
    args = parser.parse_args()

    if args.mode in ("retrieval", "all"):
        print("=== Retrieval: chunk size comparison ===")
        evaluate_retrieval(args.chunk_sizes, args.top_k)
    if args.mode in ("answers", "all"):
        print("\n=== End-to-end answer evaluation ===")
        evaluate_answers(args.top_k, args.delay)


if __name__ == "__main__":
    main()
