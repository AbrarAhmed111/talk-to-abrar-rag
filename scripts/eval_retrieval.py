"""
Runs the Phase 3 eval set (scripts/eval_questions.py) through RAGPipeline.retrieve()
and reports top-1 / top-3 hit rate against each question's expected source file.

Run with: uv run python scripts/eval_retrieval.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.eval_questions import EVAL_QUESTIONS
from src.app.core.config import get_settings
from src.app.rag.pipeline import RAGPipeline


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    settings = get_settings()

    pipeline = RAGPipeline(
        knowledge_dir=settings.resolved_knowledge_path,
        top_k=3,
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
    )
    pipeline.initialize()

    top1_hits = 0
    top3_hits = 0

    for case in EVAL_QUESTIONS:
        question = case["question"]
        expected = case["expected_source"]

        result = pipeline.retrieve(question, top_k=3)
        sources = [chunk.source for chunk in result.chunks]
        scores = result.scores

        top1_hit = bool(sources) and sources[0] == expected
        top3_hit = expected in sources
        top1_hits += int(top1_hit)
        top3_hits += int(top3_hit)

        mark = "OK  " if top3_hit else "MISS"
        print(f"[{mark}] {question}")
        print(f"       expected: {expected}")
        print(f"       got:      {list(zip(sources, [round(s, 3) for s in scores]))}")
        print(f"       relevant: {result.has_relevant_context}")

    total = len(EVAL_QUESTIONS)
    print(f"\nTop-1 hit rate: {top1_hits}/{total} ({100 * top1_hits / total:.0f}%)")
    print(f"Top-3 hit rate: {top3_hits}/{total} ({100 * top3_hits / total:.0f}%)")


if __name__ == "__main__":
    main()
