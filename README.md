# AI Engineering Lab

A hands-on lab for learning AI engineering with **local models only**. Every experiment runs against [Ollama](https://ollama.com) inside a GPU-enabled dev container. Each one is a small script built around one concept: sampling parameters, prompt engineering, structured output, LLM security, embeddings, or retrieval-augmented generation (RAG).

The lab follows a chapter-based learning path. Each chapter adds a folder of self-contained experiments.

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU with the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/) (optional; see [CPU fallback](ENVIRONMENT.md#fallback-to-cpu))
- VS Code with the Dev Containers extension

### 1. Open the dev container

Open the repository in VS Code and choose **Dev Containers: Reopen in Container**. This starts two services:

| Service  | Purpose                                                        |
|----------|----------------------------------------------------------------|
| `app`    | Python 3.11+ workspace; dependencies installed with `uv sync`  |
| `ollama` | Local model server with GPU passthrough, models kept in a Docker volume |

The `app` container shares the Ollama network namespace, so the API is available at `http://localhost:11434`.

### 2. Pull the models

```bash
docker compose -f .devcontainer/docker-compose.yml exec ollama ollama pull llama3.2:3b
```

| Model               | Used by                                    |
|---------------------|--------------------------------------------|
| `llama3.2:3b`       | Basics, simple prompting, RAG answers      |
| `ministral-3:8b`    | Persona, chain-of-thought corruption       |
| `ministral-3:14b`   | Adversarial input, chain-of-thought        |
| `mxbai-embed-large` | All embedding / vector-store experiments   |
| `llama-guard3:8b`, `qwen2.5:14b` | Audit models in `chain_of_thought_corruption.py` |

On a 4 GB GPU, stick to the 3B models. See [ENVIRONMENT.md](ENVIRONMENT.md#model-size-guidelines) for sizing guidance.

### 3. Validate the environment

```bash
uv run validate_environment.py
uv run test_ollama.py
```

---

## Repository Layout

```
.
├── .devcontainer/          # Dockerfile, compose file, VS Code dev container config
├── ENVIRONMENT.md          # Hardware, GPU/WSL2 setup, troubleshooting, security boundaries
├── validate_environment.py # Environment health check
├── test_ollama.py          # Ollama connectivity + smoke-test inference
├── ollama_models.py        # List installed models with size and quantization
├── ollama_get_models.py    # Pull a model with streamed progress
├── temperature_experiment.py
├── prompt_engineering/     # Chapter 5
│   └── security_prompts/   # Reusable LLM security review prompts
└── rag/                    # Chapter 6
    └── policies/           # Sample policy corpus for the RAG pipeline
```

---

## Experiments

### Foundations

| Script | What it shows |
|--------|---------------|
| [temperature_experiment.py](temperature_experiment.py) | The same factual question at temperature 0.0, 0.7, and 1.2 |
| [ollama_models.py](ollama_models.py) | Listing local models through the Python client |

### Chapter 5: Prompt Engineering

| Script | Technique |
|--------|-----------|
| [output_format.py](prompt_engineering/output_format.py) | Moving from free text to JSON to typed JSON fields |
| [provide_examples.py](prompt_engineering/provide_examples.py) | Few-shot prompting to steer tone and answer style |
| [adopt_persona.py](prompt_engineering/adopt_persona.py) | Persona system prompts plus Pydantic-parsed essay scoring |
| [chain_of_thought.py](prompt_engineering/chain_of_thought.py) | Step-by-step reasoning followed by a self-verification pass |
| [chain_of_thought_corruption.py](prompt_engineering/chain_of_thought_corruption.py) | Injecting logic errors into reasoning and checking whether audit models catch them; traced with Langfuse |
| [adversarial.py](prompt_engineering/adversarial.py) | Format-breaking adversarial input and retry/fallback parsing |
| [instructor_test.py](prompt_engineering/instructor_test.py) | Structured extraction with `instructor` |

**Security prompts** ([prompt_engineering/security_prompts/](prompt_engineering/security_prompts/)) are reusable review templates for prompt injection detection, few-shot poisoning, context-window manipulation, agentic tool-use risk, output validation gaps, training-data extraction risk, and generating security test cases.

### Chapter 6: Retrieval-Augmented Generation

Run these scripts from inside `rag/`. They use relative paths for `policies/`, `db/`, and `wiki_california.txt`.

| Script | Concept |
|--------|---------|
| [chroma_test.py](rag/chroma_test.py) | ChromaDB basics: upsert, chunking a long document, querying |
| [similarity_search.py](rag/similarity_search.py) | Semantic search with `mxbai-embed-large` embeddings |
| [chunking_strategies_testing.py](rag/chunking_strategies_testing.py) | Recursive vs. semantic chunking compared on the same text |
| [rag_ingest.py](rag/rag_ingest.py) | Ingestion pipeline: load Markdown and PDF, chunk, enrich metadata, persist to `db/` |
| [rag_integration.py](rag/rag_integration.py) | Full RAG engine: retrieval, context assembly, cited answers, citation verification |
| [rag_debug.py](rag/rag_debug.py) | Inspecting stored chunks by `chunk_id` |

Typical RAG flow:

```bash
cd rag
uv run rag_ingest.py        # build the vector store from policies/
uv run rag_integration.py   # ask questions and get cited, verified answers
```

The `policies/` corpus is synthetic. It deliberately contains several versions of the same policy and a legacy exception addendum, which makes it useful for testing retrieval with conflicting or outdated sources.

---

## Tooling

- **Ollama**: local inference and embeddings
- **LangChain** (`langchain-ollama`, `langchain-chroma`): prompts, parsers, and chains
- **ChromaDB**: vector store
- **Pydantic / Instructor**: structured output
- **Langfuse**: tracing and observability
- **`llm` CLI** (with `llm-ollama`): quick prompts from the terminal
- **uv**: dependency and environment management

### Configuration

Secrets go in `.env`, which is gitignored. Langfuse tracing needs:

```bash
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_SECRET_KEY=...
LANGFUSE_HOST=...
```

---

## Versioning

The version shows where the lab stands in the learning path: `PHASE.CHAPTER.PATCH`.

| Part | Meaning | Bump when |
|------|---------|-----------|
| `PHASE` (major) | Curriculum phase from the [12-week program](ENVIRONMENT.md#learning-path-context) | A new phase starts; reset the other parts |
| `CHAPTER` (minor) | Chapter of Chip Huyen's *AI Engineering* (O'Reilly) the lab has reached | A chapter's experiments are complete |
| `PATCH` | Fixes, docs, dependency or model updates | Anything that adds no new chapter content |

| Phase | Weeks | Focus |
|-------|-------|-------|
| 1 | 1–4 | Foundations + RAG |
| 2 | 5–8 | Evaluation + Agents + Production |
| 3 | 9–12 | Fine-tuning + Optimization |

`MINOR` is the actual book chapter number, so it can skip values (1.2 → 1.5 → 1.6) and keeps counting when the phase changes. A new phase starting with Chapter 7 is `2.7.0`, not `2.0.0`. `X.0.0` is used only for a phase milestone with no chapter attached, such as `1.0.0` for the lab scaffold at the start of phase 1.

Each release is an annotated git tag `vX.Y.Z`, the version in `pyproject.toml` matches the tag, and [CHANGELOG.md](CHANGELOG.md) lists the changes.

---

## Security Boundaries

This is a learning lab. Use only synthetic or public data. Never put production API keys or customer data here. The full rules for each machine are in [ENVIRONMENT.md](ENVIRONMENT.md#security-boundaries).

---

## Further Reading

- [ENVIRONMENT.md](ENVIRONMENT.md): hardware profiles, WSL2 GPU passthrough, troubleshooting
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [LangChain docs](https://python.langchain.com/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
