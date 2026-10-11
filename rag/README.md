# RAG: Policy Q&A with Verified Citations

Answers questions about the security policies in `policies/` using a local Ollama + ChromaDB pipeline.

- **Ingest** (`rag_ingest.py`): loads `policies/*.md` and `*.pdf`, splits them into 600-char chunks (200 overlap), tags each with `source` + `chunk_id`, embeds with `mxbai-embed-large`, and stores them in `db/`.
- **Retrieve** (`rag_integration.py`): finds the top-k (default 3) chunks by relevance score and numbers them as `Source [N]` in the prompt context.
- **Generate**: `llama3.2:3b` (temperature 0) answers using only the sources and must cite every claim inline as `[Source N]`.
- **Verify**: `verify_citations` checks each cited sentence's word overlap with its chunk (>25% = SUPPORTED); `check_uncited_sources` flags chunks used but never cited.

**Run** (inside the dev container, from `rag/`): `ollama pull mxbai-embed-large && ollama pull llama3.2:3b`, then `uv run rag_ingest.py` (idempotent: it rebuilds the collection with deterministic IDs, so re-running never duplicates chunks), then `uv run rag_integration.py` to run the sample questions.

## Data and attribution

- **`policies/`**: synthetic. The organisation and every policy were fabricated for RAG testing; each file carries a `SYNTHETIC` banner under its title. The banner is part of the corpus (it is chunked, embedded and retrievable), so it can show up in retrieved context and answers.
- **`wiki_california.txt`**: plain-text copy of the Wikipedia article [California](https://en.wikipedia.org/wiki/California) by Wikipedia contributors, licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Added to this repo on 2026-03-02; used by `chroma_test.py` and `chunking_strategies_testing.py`; the article's revision history is at https://en.wikipedia.org/w/index.php?title=California&action=history.
