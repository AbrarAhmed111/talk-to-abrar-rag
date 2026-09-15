"""
Manual retrieval eval set for the real knowledge base (Phase 3 of
RAG_IMPLEMENTATION_PLAN.md). Each entry is a realistic visitor question mapped
to the source file it should surface. Kept as plain data so Phase 9 can reuse
it as a parametrized regression test.
"""

EVAL_QUESTIONS = [
    {"question": "What is DevAbby?", "expected_source": "devabby.md"},
    {"question": "Who created DevAbby and why?", "expected_source": "devabby.md"},
    {"question": "What tech stack does he use for FastAPI backends?", "expected_source": "skills.md"},
    {"question": "What frontend frameworks and libraries does he work with?", "expected_source": "skills.md"},
    {"question": "Tell me about BizTradeHub.", "expected_source": "projects/biztradehub.md"},
    {"question": "What is MamtaAI and what problem does it solve?", "expected_source": "projects/mamtaai.md"},
    {"question": "What was his role on the BuyCex project?", "expected_source": "projects/buycex.md"},
    {"question": "What did he build for HolidaysUnlocked?", "expected_source": "projects/holidaysunlocked.md"},
    {"question": "What did he personally build for PromptGraphy?", "expected_source": "projects/promptgraphy.md"},
    {"question": "What is the GreenFace eCommerce project?", "expected_source": "projects/other-projects.md"},
    {"question": "How many public GitHub repositories has Abrar published?", "expected_source": "achievements.md"},
    {"question": "Where did Abrar study Computer Science?", "expected_source": "education.md"},
    {"question": "What did he study at PGC before university?", "expected_source": "education.md"},
    {"question": "What was his role at WebWhiz?", "expected_source": "career.md"},
    {"question": "How many developers has Abrar mentored?", "expected_source": "career.md"},
    {"question": "What open-source boilerplates has he published under DevAbby?", "expected_source": "developer-resources.md"},
    {"question": "Is Abrar available for freelance work right now?", "expected_source": "faq.md"},
    {"question": "How can I get in touch with him about a project?", "expected_source": "faq.md"},
    {"question": "What is Abrar's professional title and years of experience?", "expected_source": "profile.md"},
    {"question": "What do his clients say about working with him?", "expected_source": "testimonials.md"},
]
