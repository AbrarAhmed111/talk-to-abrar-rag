<div align="center">

<a href="https://www.abrarahmed.pro" target="_blank">
  <img src="https://www.abrarahmed.pro/assets/devAbby-fulllogo-C9-MX7QK.png" alt="Built by Abrar Ahmed" height="65" />
</a>

# Abrar's Reflection — RAG Backend

**The Retrieval-Augmented Generation backend powering "Talk To Abrar's Reflection"** — the AI chat feature on [abrarahmed.pro](https://www.abrarahmed.pro) that answers visitor questions about Abrar Ahmed's career, projects, and skills, grounded in his real knowledge base instead of guessing.

Built by **[Abrar Ahmed](https://www.abrarahmed.pro)** | Managed with [uv](https://docs.astral.sh/uv/)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Package Manager](https://img.shields.io/badge/managed%20by-uv-DE5FE9.svg?logo=astral&logoColor=white)](https://docs.astral.sh/uv/)
[![Built By](https://img.shields.io/badge/author-Abrar%20Ahmed-black.svg)](https://www.abrarahmed.pro)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## What This Is

A FastAPI service that turns a static Markdown knowledge base into a grounded, streaming chatbot. It is **not** a generic starter template — every document, prompt, and guardrail in this repo is written specifically for Abrar Ahmed's portfolio.

The request path is a single deterministic pipeline, not an agent:

```
user message
    ↓
[Intent Detection]     — regex match on greetings/thanks/etc? → instant canned reply, 0 LLM tokens
    ↓ no match
[BM25 Retrieval]       — keyword search over knowledge/*.md, top-k chunks
    ↓
[Context Assembly]     — format retrieved chunks + Abrar's Reflection persona into a system prompt
    ↓
[LLM Gateway]          — invoke the best available provider, with automatic failover
    ↓
streamed reply + cited source files
```

No ReAct loops, no tool-calling by the LLM, no multi-hop retrieval.

---

## Core Components

### RAG Pipeline (`src/app/rag/`)
- **Ingestion** (`ingestion/loader.py`) — walks `knowledge/` for `.md`/`.txt` files.
- **Chunking** (`chunking/text_splitter.py`) — LangChain `MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter`, heading-aware.
- **Retrieval** (`retrieval/vector_store.py`) — `InMemoryBM25VectorStore`: pure BM25 keyword/lexical scoring, zero embeddings, zero external API calls. A good fit for a small, hand-curated, ~150-chunk knowledge base.
- **Context Assembly** (`context/builder.py`) — builds the "Abrar's Reflection" persona prompt and formats retrieved chunks into a background-knowledge block.
- **Orchestration** (`pipeline.py`) — `RAGPipeline` ties the above into one `build_prompt_context(query)` call.

### Intent Detection (`src/app/intent/`)
Zero-LLM, offline regex classifier for conversational shortcuts (greetings, thanks, "who are you", etc.) so those never cost an LLM call. Anything substantive falls through to the RAG pipeline.

### LLM Gateway (`src/app/gateway/`)
Multi-provider failover across **Gemini** (up to 4 rotated keys + a quality-fallback model), **Groq**, **OpenAI**, **Mistral**, and **Cerebras** — all via LangChain's `ChatOpenAI` against each provider's OpenAI-compatible endpoint. On a rate-limit/quota/5xx error it cools the deployment down and tries the next one; on an invalid key or missing model it disables that deployment permanently for the process lifetime.

### Chat Service (`src/app/services/chat_service.py`)
Orchestrates: intent check → (canned reply) or (RAG context → gateway call) → response, for both the standard JSON endpoint and the SSE streaming endpoint.

---

## Project Structure

```
talk-to-abrar-rag/
├── knowledge/                        # The actual knowledge base (source of truth)
│   ├── profile.md                    # Identity, contact, privacy boundary
│   ├── career.md                     # Employment history & mentorship
│   ├── skills.md                     # Technical skills
│   ├── education.md                  # Academic background
│   ├── achievements.md               # Quantified highlights
│   ├── devabby.md                    # DevAbby brand identity
│   ├── developer-resources.md        # Open-source boilerplates & templates
│   ├── faq.md                        # Availability, contact, rates
│   ├── testimonials.md               # Client testimonials
│   ├── projects/                     # One file per case-study project
│   └── README.md                     # Knowledge base authoring guide
│
├── src/app/
│   ├── main.py                       # FastAPI app + lifespan (indexes RAG on startup)
│   ├── api/routes/                   # chat.py (POST /api/chat, /api/chat/stream), health.py
│   ├── core/                         # config.py (pydantic-settings), logging.py
│   ├── services/chat_service.py      # Orchestrates intent → RAG → LLM gateway
│   ├── rag/                          # Ingestion, chunking, retrieval, context assembly, pipeline
│   ├── gateway/                      # Multi-provider LLM client + failover
│   ├── intent/                       # Rule-based intent classifier + canned responses
│   └── schemas/                      # Pydantic request/response models
│
├── scripts/                          # Dev-only eval tooling (not part of the test suite)
│   ├── eval_questions.py             # Question → expected-source regression set
│   ├── eval_retrieval.py             # Runs the eval set, reports top-1/top-3 hit rate
│   └── inspect_chunks.py             # Dumps chunk boundaries for manual review
│
├── tests/                            # pytest suite (fully mocked, 0 real tokens)
├── run.py                            # Dev entrypoint (uvicorn, hot-reload)
├── pyproject.toml                    # Dependencies & tool config (uv-managed)
├── .env.example                      # Environment variable template
└── RAG_IMPLEMENTATION_PLAN.md        # Phase-by-phase design & build log
```

---

## Quickstart

### 1. Install [uv](https://docs.astral.sh/uv/)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Set up the environment

```bash
cd talk-to-abrar-rag
cp .env.example .env
uv sync
```

Edit `.env` and set at least one provider key (`GOOGLE_API_KEY1`, `GROQ_API_KEY`, `OPENAI_API_KEY`, `MISTRAL_API_KEY`, or `CEREBRAS_API_KEY`). The gateway only needs one working key to function — the rest are optional failover targets.

### 3. Run the server

```bash
uv run python run.py
# or
uv run uvicorn src.app.main:app --reload
```

- API root: http://localhost:8000/
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

The knowledge base under `knowledge/` is loaded, chunked, and indexed automatically on startup — no separate ingestion step.

---

## API Endpoints

### `POST /api/chat` — standard JSON completion
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is DevAbby?"}], "temperature": 0.7}'
```
Response includes `reply`, `provider`, `model`, `usage`, `intent`, `sources` (cited knowledge-base files), and `status_events` (any provider fallbacks that occurred).

### `POST /api/chat/stream` — Server-Sent Events streaming
```bash
curl -N -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Tell me about his projects"}]}'
```
Streams `delta` events with reply tokens, optional `status` events on provider fallback, and one final `done` event carrying the same fields as the JSON endpoint's response.

### `GET /health`
Reports gateway deployment availability and live RAG index status (`indexed_chunks`, source path).

---

## Configuration (`.env`)

See `.env.example` for the full template. Key groups:

| Group | Variables |
|---|---|
| App | `APP_NAME`, `ENVIRONMENT`, `LOG_LEVEL`, `HOST`, `PORT` |
| CORS | `ALLOWED_ORIGINS` — must include the production frontend origin (`https://www.abrarahmed.pro`) alongside local dev origins |
| Identity | `ASSISTANT_NAME` — the persona name used in the system prompt |
| RAG | `KNOWLEDGE_BASE_PATH`, `RAG_TOP_K`, `RAG_CHUNK_SIZE`, `RAG_CHUNK_OVERLAP` |
| Gateway | `GATEWAY_MAX_ATTEMPTS`, `GATEWAY_COOLDOWN_SECONDS` |
| Providers | `GOOGLE_API_KEY1..4` + `GEMINI_MODEL`/`GEMINI_FALLBACK_MODEL`, `GROQ_API_KEY` + `GROQ_MODEL`/`GROQ_FALLBACK_MODEL`, `OPENAI_API_KEY` + `OPENAI_MODEL`, `MISTRAL_API_KEY` + `MISTRAL_MODEL`, `CEREBRAS_API_KEY` + `CEREBRAS_MODEL` |

---

## Updating the Knowledge Base

Add or edit Markdown files directly under `knowledge/` (see `knowledge/README.md` for authoring guidelines — heading structure, chunk-friendly formatting). Changes take effect on the next server start; there's no separate build/ingestion step.

To sanity-check retrieval quality after a knowledge base change:

```bash
uv run python scripts/eval_retrieval.py
```

This runs the curated question set in `scripts/eval_questions.py` against the live index and reports top-1/top-3 hit rate.

---

## Testing

```bash
uv run pytest              # full suite
uv run pytest -v tests/test_rag.py   # a single file
```

All tests are fully mocked at the LLM boundary — no real API tokens are consumed.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Built By

**[Abrar Ahmed](https://www.abrarahmed.pro)** — Full Stack Engineer

<a href="https://www.abrarahmed.pro" target="_blank">
  <img src="https://www.abrarahmed.pro/assets/devAbby-fulllogo-C9-MX7QK.png" alt="devAbby logo" height="50" />
</a>
