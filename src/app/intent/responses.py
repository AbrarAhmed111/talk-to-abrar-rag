"""
Generic Canned Responses for Non-LLM Intents.
Kept strictly separate from detection logic.
Returns fast local answers for common conversational interactions (0 LLM cost).

EXTENSION GUIDE:
To add custom domain intents and responses:
1. Define your intent constant in `types.py` (e.g. `INTENT_BUSINESS_HOURS = "business_hours"`).
2. Add regex pattern rules in `detector.py`.
3. If the answer is static, add your canned answer below in `CANNED_RESPONSES`.
   If it requires RAG or dynamic generation, set `should_use_llm = True` in `detector.py`.
"""

from typing import Dict
from .types import (
    INTENT_GREETING,
    INTENT_WELLBEING,
    INTENT_BOT_IDENTITY,
    INTENT_COMPLIMENT,
    INTENT_PLEASANTRY,
    INTENT_APOLOGY,
    INTENT_PING,
    INTENT_THANKS,
    INTENT_GOODBYE,
    INTENT_ACKNOWLEDGEMENT,
    INTENT_CONFIRMATION,
    INTENT_SIMPLE_NEGATIVE,
    INTENT_SIMPLE_POSITIVE,
    INTENT_CANCELLATION,
    INTENT_SIMPLE_CLARIFICATION,
    INTENT_CAPABILITY_HELP,
)

CANNED_RESPONSES: Dict[str, str] = {
    INTENT_GREETING: (
        "Hey! I'm Abrar's Reflection — here to talk about Abrar Ahmed's work, projects, and background as a Full Stack Engineer. What would you like to know?"
    ),
    INTENT_WELLBEING: (
        "I'm doing great, thank you for asking! I'm here to help with Abrar Ahmed's profile, work, projects, and technical background. What would you like to know?"
    ),
    INTENT_BOT_IDENTITY: (
        "I'm Abrar's Reflection — built to speak on behalf of Abrar Ahmed about his experience, full-stack engineering work, AI projects, the DevAbby brand, and his portfolio. You can explore more at https://abrarahmed.pro."
    ),
    INTENT_COMPLIMENT: (
        "Thank you! Happy to help — let me know if you'd like to know more about Abrar's work or projects."
    ),
    INTENT_PLEASANTRY: (
        "Nice to meet you! Feel free to ask about Abrar's background, projects, or skills."
    ),
    INTENT_APOLOGY: (
        "No problem at all! How can I assist you today?"
    ),
    INTENT_PING: (
        "I'm online and ready! What would you like to know?"
    ),
    INTENT_THANKS: (
        "You're very welcome! Let me know if there is anything else I can help you with."
    ),
    INTENT_GOODBYE: (
        "Goodbye! Have a great day, and feel free to return whenever you need assistance."
    ),
    INTENT_ACKNOWLEDGEMENT: (
        "Understood. Let me know what you would like to explore next."
    ),
    INTENT_CONFIRMATION: (
        "Great! Let me know if you have any other questions."
    ),
    INTENT_SIMPLE_NEGATIVE: (
        "No problem. Let me know if anything else comes up."
    ),
    INTENT_SIMPLE_POSITIVE: (
        "Wonderful! How else can I assist you?"
    ),
    INTENT_CANCELLATION: (
        "Operation cancelled. What else can I help you with?"
    ),
    INTENT_SIMPLE_CLARIFICATION: (
        "Could you please specify which topic or feature you would like me to explain?"
    ),
    INTENT_CAPABILITY_HELP: (
        "I can help you with:\n"
        "• Abrar Ahmed’s background, experience, and education\n"
        "• Full-stack engineering, AI, and product development work\n"
        "• DevAbby projects, portfolio, and professional identity\n"
        "• Technical skills, leadership background, and mentoring experience\n\n"
        "What would you like to know about Abrar or his work?"
    ),
}


def get_canned_response(intent: str) -> str:
    """
    Retrieve canned response text for a non-LLM intent.
    Falls back to a polite generic prompt if intent is not recognized.
    """
    return CANNED_RESPONSES.get(
        intent,
        "How can I assist you today?"
    )
