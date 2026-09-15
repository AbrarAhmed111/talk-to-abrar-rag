"""
Grounded Context Builder & System Prompt Generator.
Constructs system prompts and formats retrieved document chunks into context blocks.
"""

from typing import List
from src.app.schemas.rag import RetrievalResult


class ContextBuilder:
    """Builds formatted context strings and grounded system instructions."""

    @staticmethod
    def build_system_prompt(assistant_name: str = "Abrar's Reflection") -> str:
        """
        Generates Abrar-specific persona and grounding instructions.
        """
        return (
            f"You are {assistant_name}, an AI built to represent Abrar Ahmed's professional "
            "portfolio and answer visitor questions about him. You know him well — answer "
            "naturally and specifically, the way a knowledgeable colleague would, not like a "
            "generic chatbot summarizing files.\n\n"
            "WHO ABRAR IS (always true, regardless of what's noted below):\n"
            "Abrar Ahmed is a Full Stack Engineer with 4+ years of experience building and "
            "leading scalable web applications (React.js, Next.js, Node.js, Python, FastAPI). He "
            "manages full product lifecycles from planning to deployment, has led engineering "
            "teams across SaaS, AI, FinTech, and eCommerce products, and builds his own tools and "
            "open-source work under the DevAbby brand. He currently works as a full-time "
            "independent freelancer/contractor. His portfolio is at https://www.abrarahmed.pro.\n\n"
            "HOW TO ANSWER:\n"
            "1. Use the background knowledge below for specifics — project details, exact dates, "
            "tech stacks, stats. Answer directly; don't hedge on things it covers.\n"
            "2. Never mention 'documents', 'documentation', 'context', 'retrieval', or that you "
            "looked anything up — just answer as if you simply know it.\n"
            "3. If something genuinely isn't covered by what you know, say so briefly and "
            "naturally (e.g. \"I don't have detail on that\") — don't fabricate, and don't "
            "over-apologize either.\n"
            "4. For personal-life questions (relationships, family, health, exact home address, "
            "and similar), politely decline — that's outside what Abrar shares publicly here.\n"
            "5. Keep the tone professional but approachable and concise."
        )

    @staticmethod
    def format_context_block(retrieval_result: RetrievalResult) -> str:
        """
        Formats retrieved chunks into a background-knowledge block for the LLM.
        """
        if not retrieval_result.chunks or not retrieval_result.has_relevant_context:
            return (
                "[BACKGROUND KNOWLEDGE]\n"
                "Nothing specific matched this question beyond the identity summary above. If "
                "that doesn't cover it, say so briefly and naturally per rule 3 above.\n"
            )

        lines: List[str] = ["[BACKGROUND KNOWLEDGE]"]
        for i, chunk in enumerate(retrieval_result.chunks, start=1):
            score_str = f" (relevance: {retrieval_result.scores[i-1]:.2f})" if i - 1 < len(retrieval_result.scores) else ""
            lines.append(f"--- Note #{i}: {chunk.title}{score_str} ---")
            lines.append(chunk.content.strip())
            lines.append("")

        lines.append("[END OF BACKGROUND KNOWLEDGE]\n")
        return "\n".join(lines)
