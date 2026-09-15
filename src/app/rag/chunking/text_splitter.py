"""
Markdown Text Splitter.
Thin wrapper around LangChain's header-aware and recursive-character
splitters, producing DocumentChunk objects with source and heading metadata.
"""

from typing import Dict, List
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from src.app.schemas.rag import DocumentChunk

HEADERS_TO_SPLIT_ON = [("#", "h1"), ("##", "h2"), ("###", "h3"), ("####", "h4")]


class MarkdownTextSplitter:
    """
    Splits markdown text into DocumentChunk objects in two passes:
    1. MarkdownHeaderTextSplitter groups text under its nearest heading, so a
       chunk never mixes content from two different sections.
    2. RecursiveCharacterTextSplitter breaks any section that's still over
       chunk_size into smaller pieces, preferring paragraph/line/word
       boundaries so it never cuts a sentence or list item mid-way.
    """

    def __init__(self, chunk_size: int = 700, chunk_overlap: int = 120):
        self.header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=HEADERS_TO_SPLIT_ON, strip_headers=False
        )
        self.size_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_document(self, text: str, source: str) -> List[DocumentChunk]:
        """Splits markdown text into DocumentChunk objects with source and heading metadata."""
        if not text or not text.strip():
            return []

        chunks: List[DocumentChunk] = []
        chunk_idx = 0

        for section in self.header_splitter.split_text(text):
            title = self._title(section.metadata)
            for piece in self.size_splitter.split_text(section.page_content):
                piece = piece.strip()
                if not piece:
                    continue
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{source}#chunk-{chunk_idx}",
                        source=source,
                        title=title,
                        content=piece,
                        metadata={"chunk_index": chunk_idx},
                    )
                )
                chunk_idx += 1

        return chunks

    @staticmethod
    def _title(metadata: Dict[str, str]) -> str:
        """Uses the deepest heading level present as the chunk's title."""
        for level in ("h4", "h3", "h2", "h1"):
            if level in metadata:
                return metadata[level]
        return "General"
