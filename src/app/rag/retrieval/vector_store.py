"""
Vector Store and Retrieval Engine.
Provides an out-of-the-box in-memory BM25 (keyword/lexical) search index with
pluggable extension points for production vector databases
(PostgreSQL + pgvector, Chroma, Pinecone, Qdrant) or an embeddings-based store.
"""

import math
import logging
from abc import ABC, abstractmethod
from typing import List, Tuple
from collections import Counter
from src.app.schemas.rag import DocumentChunk, RetrievalResult

logger = logging.getLogger("RAGRetriever")

# Common English filler words carry little topical signal but still add up
# in BM25's score, especially against short chunks (e.g. FAQ answers phrased
# as questions like "Does he do full-time roles?") where a few overlapping
# filler words with the query can outweigh the one real keyword match.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "so", "of", "in", "on", "for",
    "to", "with", "about", "into", "at", "by", "from", "is", "are", "was",
    "were", "be", "been", "being", "do", "does", "did", "has", "have", "had",
    "he", "she", "it", "they", "his", "her", "him", "them", "their", "what",
    "who", "how", "why", "which", "when", "where", "this", "that", "these",
    "those", "you", "your", "can", "will", "would", "should", "could", "as",
    # Conversational filler ("tell me about X", "let me know", "please give
    # me") that otherwise incidentally matches the first-person narrative
    # prose used throughout the knowledge base (e.g. "...shaped me into the
    # engineer I am today"), pulling in unrelated chunks for no topical reason.
    "tell", "me", "please", "know", "give", "get", "want",
}


class BaseVectorStore(ABC):
    """Abstract interface for RAG vector index backends."""

    @abstractmethod
    def add_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Indexes document chunks."""
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> RetrievalResult:
        """Searches index for most relevant chunks given a query."""
        pass


class InMemoryBM25VectorStore(BaseVectorStore):
    """
    Default lightweight in-memory BM25 (keyword/lexical) search store.
    Scores chunks by BM25 term weighting alone — no embeddings or vector
    similarity are computed. For a small, hand-curated knowledge base this is
    a zero-cost, fully deterministic retrieval strategy that needs no external
    API calls. It does not do semantic/paraphrase matching, so a future
    embeddings-based store (see EXTENSION GUIDE) could combine BM25 with
    cosine similarity for a true hybrid search if that's ever needed.

    EXTENSION GUIDE:
    To swap in pgvector:
    1. Create `app/rag/retrieval/pgvector_store.py` inheriting from `BaseVectorStore`.
    2. Implement `add_chunks` to insert embeddings into your PostgreSQL table.
    3. Implement `search` with `SELECT ... ORDER BY embedding <=> query_embedding LIMIT top_k`.
    """

    # profile.md is the one file that answers generic identity questions
    # ("Who is Abrar?", "Tell me about him") — but those queries carry almost
    # no distinguishing keyword signal (the corpus mentions his name
    # everywhere), so plain BM25 often ranks a weaker incidental match above
    # it. A small deterministic boost (tuned empirically — 1.6x already
    # overpowered dedicated matches like devabby.md's own "What is DevAbby?"
    # chunk; 1.2x fixes identity queries without disturbing anything else)
    # nudges it back to the top for exactly that narrow case.
    PROFILE_SOURCE = "profile.md"
    PROFILE_BOOST = 1.2

    def __init__(self, relevance_threshold: float = 1.0):
        # Tuned against the Phase 3 eval set (scripts/eval_retrieval.py): raw
        # BM25 scores here range roughly 4.5-30+ for genuine matches and 0 for
        # queries with zero term overlap, so 1.0 comfortably separates "no
        # overlap at all" from a real match without rejecting a weak-but-real
        # one. It's a floor, not a topic filter — a query with an incidental
        # word overlap can still score a few points (e.g. a personal-life
        # question that happens to share a word with the corpus), so it's not
        # relied on to enforce the privacy boundary; that's a system-prompt
        # instruction (Phase 6), not a retrieval-time score cutoff.
        self.chunks: List[DocumentChunk] = []
        self.doc_freqs: Counter = Counter()
        self.chunk_term_counts: List[Counter] = []
        self.chunk_lengths: List[int] = []
        self.avg_doc_len: float = 1.0
        self.total_docs: int = 0
        self.relevance_threshold = relevance_threshold

    def _tokenize(self, text: str) -> List[str]:
        """Simple alphanumeric tokenizer, lowercaser, and stopword filter."""
        import re
        tokens = re.findall(r"\b[a-zA-Z0-9_-]{2,}\b", text.lower())
        return [t for t in tokens if t not in STOPWORDS]

    def add_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Indexes chunks in memory."""
        self.chunks.extend(chunks)
        self.total_docs = len(self.chunks)

        for chunk in chunks:
            full_text = f"{chunk.title} {chunk.content}"
            tokens = self._tokenize(full_text)
            term_counts = Counter(tokens)
            self.chunk_term_counts.append(term_counts)
            self.chunk_lengths.append(len(tokens))
            for term in term_counts.keys():
                self.doc_freqs[term] += 1

        total_length = sum(self.chunk_lengths)
        self.avg_doc_len = (total_length / self.total_docs) if self.total_docs > 0 else 1.0

    def search(self, query: str, top_k: int = 3) -> RetrievalResult:
        """
        Executes BM25-based semantic scoring over indexed chunks.
        """
        if not self.chunks or not query.strip():
            return RetrievalResult(query=query, chunks=[], scores=[], has_relevant_context=False)

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return RetrievalResult(query=query, chunks=[], scores=[], has_relevant_context=False)

        scores: List[Tuple[int, float]] = []
        k1 = 1.5
        b = 0.75

        for idx in range(self.total_docs):
            doc_len = self.chunk_lengths[idx]
            term_counts = self.chunk_term_counts[idx]
            doc_score = 0.0

            for q_term in query_tokens:
                if q_term in term_counts:
                    tf = term_counts[q_term]
                    df = self.doc_freqs.get(q_term, 1)
                    # Standard BM25 IDF
                    idf = math.log(1.0 + (self.total_docs - df + 0.5) / (df + 0.5))
                    # Term saturation with document length normalization
                    num = tf * (k1 + 1.0)
                    den = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))
                    doc_score += idf * (num / den)

            if self.chunks[idx].source == self.PROFILE_SOURCE:
                doc_score *= self.PROFILE_BOOST

            scores.append((idx, doc_score))

        # Sort descending by score
        scores.sort(key=lambda x: x[1], reverse=True)

        top_candidates = scores[:top_k]
        retrieved_chunks = [self.chunks[idx] for idx, _ in top_candidates if top_candidates]
        retrieved_scores = [score for _, score in top_candidates if top_candidates]

        has_relevant = any(s >= self.relevance_threshold for s in retrieved_scores)

        return RetrievalResult(
            query=query,
            chunks=retrieved_chunks,
            scores=retrieved_scores,
            has_relevant_context=has_relevant,
        )
