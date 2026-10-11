# Changelog

Versions follow `PHASE.CHAPTER.PATCH`, which tracks progress through the curriculum and the book. See [Versioning](README.md#versioning).

## [1.6.1] - 2026-10-11

Cleanup after Chapter 6. No new chapter content.

- Rewrote README as the AI Engineering Lab overview; added a RAG README
- Pinned the Ollama image to 0.40.3 and documented every model the code uses
- Made RAG ingestion idempotent
- Switched to `langchain_chroma` from the deprecated community `Chroma`
- Added `langchain-experimental`, synthetic-data banners and data attribution
- Introduced semantic versioning and this changelog

## [1.6.0] - 2026-09-23

Chapter 6: Retrieval-Augmented Generation.

- ChromaDB basics, similarity search with `mxbai-embed-large`
- Recursive vs. semantic chunking comparison
- Ingestion pipeline (Markdown/PDF, chunking, metadata, persistence)
- RAG engine with cited answers and citation verification

## [1.5.0] - 2026-02-25

Chapter 5: Prompt Engineering.

- Output formats, few-shot examples, personas, chain-of-thought
- Adversarial input, structured extraction with `instructor`
- Chain-of-thought corruption with audit models, traced with Langfuse
- Reusable LLM security review prompts

## [1.0.0] - 2026-02-18

Phase 1 foundations: the lab environment.

- GPU-enabled dev container with Ollama
- Temperature experiment, environment validation and docs
- `llm` CLI with the Ollama plugin

[1.6.1]: https://github.com/mijoe/ailab/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/mijoe/ailab/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/mijoe/ailab/compare/v1.0.0...v1.5.0
[1.0.0]: https://github.com/mijoe/ailab/releases/tag/v1.0.0
