# Knowledge Base Directory

This folder holds the raw knowledge documents used by the RAG (Retrieval-Augmented Generation) pipeline.

## Structure

```text
knowledge/
├── profile.md               # Identity, contact, privacy boundary
├── career.md                # Employment history & mentorship
├── skills.md                # Technical skills & capabilities
├── education.md             # Academic background
├── achievements.md          # Quantified highlights & milestones
├── devabby.md                # DevAbby brand identity & initiatives
├── developer-resources.md   # Open-source boilerplates & templates
├── faq.md                   # Availability, contact, response time, rates
├── testimonials.md          # Consolidated client testimonials & satisfaction stats
├── projects/
│   ├── promptgraphy.md
│   ├── buycex.md
│   ├── holidaysunlocked.md
│   ├── biztradehub.md
│   ├── mamtaai.md
│   └── other-projects.md    # Remaining smaller/showcase projects
└── README.md
```

Files sit directly under `knowledge/` (with one `projects/` subfolder for individual case studies) — there is no `documents/` subfolder.

## How to Add Your Own Documents

1. Place any Markdown (`.md`) or plain text (`.txt`) files directly under `knowledge/` (or inside `knowledge/projects/` for a new case study).
2. The RAG ingestion loader automatically reads all files in this folder (recursively) upon startup.
3. Content is split into chunks according to `RAG_CHUNK_SIZE` and `RAG_CHUNK_OVERLAP` configured in your `.env`.
4. When a user sends a question, the retriever computes similarity scores against these chunks and injects the most relevant context into the LLM prompt.

## Best Practices for RAG Documents
- **Use Clear Headings (`#`, `##`, `###`)**: The recursive chunker uses heading boundaries to maintain coherent semantic context.
- **Group Related Concepts**: Keep FAQs, instructions, and technical specifications organized in logical subsections.
- **Include Tables or Structured Lists**: Structured markdown renders cleanly and provides high retrieval precision.
