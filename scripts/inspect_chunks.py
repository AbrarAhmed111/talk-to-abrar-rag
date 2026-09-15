"""
Manual check for the real knowledge base (Phase 2 of RAG_IMPLEMENTATION_PLAN.md).

Loads and chunks knowledge/, then prints a per-file chunk count and the full
text of every chunk so boundaries can be sanity-checked by eye.

Run with: uv run python scripts/inspect_chunks.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.app.core.config import get_settings
from src.app.rag.ingestion.loader import DocumentLoader


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    settings = get_settings()
    loader = DocumentLoader(
        directory_path=settings.resolved_knowledge_path,
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
    )
    chunks = loader.load_documents()

    counts: dict[str, int] = {}
    for chunk in chunks:
        counts[chunk.source] = counts.get(chunk.source, 0) + 1

    print(
        f"\n{len(chunks)} total chunks from {len(counts)} files "
        f"(chunk_size={settings.RAG_CHUNK_SIZE}, overlap={settings.RAG_CHUNK_OVERLAP})\n"
    )
    for source, count in sorted(counts.items()):
        print(f"  {source:<40} {count} chunks")

    print("\n--- Full chunk text (for boundary sanity-checking) ---")
    for chunk in chunks:
        print(f"\n[{chunk.chunk_id}] title={chunk.title!r} chars={len(chunk.content)}")
        print(chunk.content)


if __name__ == "__main__":
    main()
