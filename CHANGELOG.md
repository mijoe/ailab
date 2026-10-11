# Changelog

Versions follow `PHASE.CHAPTER.PATCH`, which tracks progress through the curriculum and the book (Chip Huyen, *AI Engineering*, O'Reilly 2025). See [Versioning](README.md#versioning).

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

## [1.2.1] - 2026-02-18

Environment docs and tooling after Chapter 2.

- Added ENVIRONMENT.md (hardware profiles, WSL2 GPU setup, troubleshooting)
- Added the `llm` CLI with the Ollama plugin

## [1.2.0] - 2026-02-16

Chapter 2: Understanding Foundation Models.

- Temperature experiment: the same question sampled at 0.0, 0.7 and 1.2
- Validation adjusted for the smaller work-laptop GPU

## [1.1.0] - 2026-02-15

Chapter 1: Introduction to Building AI Applications with Foundation Models.

- Local AI stack running: GPU passthrough, Python dev container, `uv` project
- Environment validation and a first inference against Ollama

## [1.0.0] - 2026-02-15

Phase 1 start: lab scaffold.

- Dev container and Docker Compose setup with an Ollama service

[1.6.1]: https://github.com/mijoe/ailab/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/mijoe/ailab/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/mijoe/ailab/compare/v1.2.1...v1.5.0
[1.2.1]: https://github.com/mijoe/ailab/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/mijoe/ailab/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/mijoe/ailab/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/mijoe/ailab/releases/tag/v1.0.0
