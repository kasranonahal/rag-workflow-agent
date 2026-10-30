# RAG Workflow Agent

A local-first retrieval-augmented generation workflow service for text and Markdown documents. Includes document ingestion, chunking, SQLite-backed storage, full-text search, source citations, and an optional OpenAI-compatible LLM endpoint. Without an LLM, the service returns relevant passages rather than fabricating an answer.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

```bash
curl -X POST http://127.0.0.1:8000/ingest -H 'Content-Type: application/json' -d '{"source":"notes.md","text":"RAG combines retrieval with language generation."}'
curl -X POST http://127.0.0.1:8000/query -H 'Content-Type: application/json' -d '{"question":"What is RAG?"}'
```

Optional model configuration: `LLM_BASE_URL` (OpenAI-compatible base URL ending in `/v1`), `LLM_API_KEY`, and `LLM_MODEL`. These are read from environment variables, never stored in the repository. `RAG_DB` sets the SQLite database path.

## Architecture

Ingest -> clean -> overlapping chunks -> SQLite FTS5 index -> retrieve top passages -> citation-aware answer. A simple workflow coordinator tracks steps in the request response. This baseline uses lexical retrieval (not vector embeddings); add an embedding index for semantic search at larger scale.

## Safety

Only use documents you are permitted to process. Retrieved documents are treated as untrusted reference text and are separated from the system instruction. Review model outputs before using them for consequential decisions.

## Tests

```bash
pytest -q
```
