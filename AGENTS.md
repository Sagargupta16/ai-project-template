# AGENTS.md

Instructions for coding agents (Claude Code, Codex, Cursor, Aider, Gemini CLI, Windsurf, Jules, Devin) working in this repository. This is the canonical agent spec; `CLAUDE.md` points here.

## What this repo is

A **unified Python template** for AI projects -- classical ML, deep learning, LLM apps, RAG, and agents. Fork it when starting a new project; do not treat it as a running application.

Python **3.13+** is required (pinned in `.python-version` and `pyproject.toml`).

## How to run things

The `Makefile` is the canonical command interface. All commands go through `uv`.

| Task | Command |
|------|---------|
| Install base | `make setup` |
| Install everything | `make dev` |
| Install specific extras | `uv sync --extra ml --extra llm --extra rag` |
| Run tests | `make test` |
| Single test | `uv run pytest tests/unit/test_dataset.py::test_preprocess_drops_duplicates -v` |
| Lint / format | `make lint` / `make format` |
| API dev server | `make api` (requires `[api]` extra) |
| Offline evals | `make eval` |
| Notebook | `make notebook` |

Available extras: `ml`, `dl`, `llm`, `rag`, `agents`, `eval`, `api`, `jupyter`, `dev`, `all`.

## Architecture (domain-separated under `src/`)

```
src/
  core/          # config, logging, utils - imported by everything
  ml/            # classical ML + DL: dataset, features, train, predict
  rag/           # chunking, indexing, retrieval
  agents/        # LLM-driven loops (plan -> tool-call -> observe)
  workflows/     # deterministic LLM pipelines (chains, routing)
  tools/         # stateless, typed callables agents can invoke
  prompts/       # versioned templates + registry
  evals/         # datasets/, offline/, judges/
  guardrails/    # input/output filters around LLM calls
  observability/ # OTel tracing, cost tracking, feedback
  services/      # business logic, DB, external APIs
  api/           # FastAPI entrypoint + routers
```

### The three bucket rule (resolve ambiguity this way)

- **`agents/`** → contains an LLM loop. Decides what to do next.
- **`tools/`** → stateless callable exposed to an agent. Pure input → output.
- **`services/`** → business logic / DB / external APIs. No LLM control flow.
- **`workflows/`** → deterministic pipelines that call LLMs but with fixed control flow.

If you're about to put a tool into `services/` or an agent into `tools/`, stop and re-read this.

## Core conventions

1. **Every `.py` file starts with `from __future__ import annotations`.** No exceptions.
2. **Config is centralized** in [src/core/config.py](src/core/config.py) as a `pydantic-settings` model with nested sub-settings (`ml`, `llm`, `rag`, `observability`). Load via `get_settings()` -- cached. Override via environment: `LLM_MODEL=claude-opus-4-7`, `RAG_TOP_K=10`, etc. Nested delimiter is `__`.
3. **Imports are absolute from project root**: `from src.core.config import get_settings`. No relative imports.
4. **Logging**: `logger = logging.getLogger(__name__)` at module top. Use `%s`-style lazy formatting: `logger.info("loaded %d rows", n)` -- never f-strings in log calls.
5. **Prompts are versioned**. Filenames: `<name>.v1.md`, `<name>.v2.md`. Register via `src.prompts.registry`. Graduate to MLflow / LangSmith / Langfuse when going to production.
6. **Evals live in `src/evals/`**: datasets as JSONL, offline runs in `offline/`, judges (LLM-as-judge or deterministic) in `judges/`.
7. **Data**: `data/raw/` is immutable. Derived artifacts go to `data/interim/` or `data/processed/`.
8. **Models artifacts** (trained weights, vector indexes) go to `models/` -- gitignored by default.

## Tooling

- **Ruff** (line 120, target py313, rules `E, F, W, I, UP, B, SIM`). `UP` will flag legacy Python -- use modern syntax (`match`, `X | None`, `pathlib`).
- **Ruff format** with double quotes. Same tool handles lint + format.
- **mypy** configured in `pyproject.toml`. Not enforced in CI yet; run locally.
- **Pre-commit** blocks files >5MB. Large data does not belong in the repo -- use DVC or cloud storage.
- **pytest-asyncio** is in auto mode. Async tests do not need decorators.

## Adding a new capability -- where does it go?

| Capability | Location |
|-----------|----------|
| New sklearn model | `src/ml/train.py` |
| New retriever (pgvector, qdrant) | `src/rag/retrieval.py` |
| Tool the agent calls (e.g. SQL query) | `src/tools/<tool_name>.py` |
| Agent with its own loop | `src/agents/<agent_name>.py` |
| Deterministic multi-step LLM flow | `src/workflows/<flow_name>.py` |
| New prompt | `src/prompts/templates/<name>.v1.md` |
| LLM-judge evaluator | `src/evals/judges/<metric>.py` |
| PII redaction rule | `src/guardrails/filters.py` |
| External API client (Stripe, Slack) | `src/services/<provider>.py` |
| REST endpoint | `src/api/routers/<resource>.py` |

## Verification protocol

Before reporting task complete:
- **Code changes**: `make lint` + `make test`. Both must pass.
- **API changes**: start `make api`, hit the endpoint with curl/httpx.
- **Eval changes**: `make eval` should run without error on the golden dataset.
- Do not report done from lint or type checks alone; run the behavior and cite what you observed.

## What not to do

- Don't mix LLM control flow into `services/`.
- Don't add `requirements.txt` entries -- everything belongs in `pyproject.toml` extras.
- Don't commit `.env`, API keys, model weights, or raw data dumps.
- Don't introduce relative imports.
- Don't skip `from __future__ import annotations`.
- Don't put helper logic inline in a notebook when it could live in `src/`.
