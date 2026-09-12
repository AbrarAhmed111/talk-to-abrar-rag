# Knowledge Base Directory

This folder holds the raw knowledge documents used by the RAG (Retrieval-Augmented Generation) pipeline.

## Structure

```text
knowledge/
├── documents/
│   ├── sample_guide.md       # Default sample knowledge document
│   └── your_document.md      # Place your project documents here (.md or .txt)
└── README.md
```

## How to Add Your Own Documents

1. Place any Markdown (`.md`) or plain text (`.txt`) files inside the `knowledge/documents/` folder.
2. The RAG ingestion loader automatically reads all files in this folder upon startup.
3. Content is split into chunks according to `RAG_CHUNK_SIZE` and `RAG_CHUNK_OVERLAP` configured in your `.env`.
4. When a user sends a question, the retriever computes similarity scores against these chunks and injects the most relevant context into the LLM prompt.

## Best Practices for RAG Documents
- **Use Clear Headings (`#`, `##`, `###`)**: The recursive chunker uses heading boundaries to maintain coherent semantic context.
- **Group Related Concepts**: Keep FAQs, instructions, and technical specifications organized in logical subsections.
- **Include Tables or Structured Lists**: Structured markdown renders cleanly and provides high retrieval precision.
