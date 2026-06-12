# AI Project Template

A unified Python starter for **every AI use case** -- classical ML, deep learning, LLM apps, RAG, and agents. One layout, optional extras, opinionated tooling.

## Why this template

Most AI templates pick a niche. Cookiecutter Data Science assumes sklearn + notebooks. Production RAG templates assume a FastAPI service with a vector store. This template assumes **your project will span several of those** (ML model → RAG retriever → agent tool → API) and gives each concern its own home without forcing you to install frameworks you don't need.

## Quick start

```bash
# Install uv (https://docs.astral.sh/uv/)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install base + the extras you need
make setup                                    # base only
uv sync --extra ml --extra llm --extra rag    # targeted
make dev                                      # everything

# Run
make test              # tests
make api               # FastAPI dev server on :8000
make eval              # offline evals on the golden dataset
make notebook          # Jupyter
```

## Extras

Base install is deliberately lean -- just `pydantic`, `pydantic-settings`, `python-dotenv`, `tqdm`. Everything heavy is an opt-in extra:

| Extra | Adds | Use when |
|-------|------|----------|
| `ml` | numpy, pandas, sklearn, matplotlib | Classical ML, data science |
| `dl` | torch | Deep learning |
| `llm` | anthropic, openai, tiktoken | Calling LLMs |
| `rag` | chromadb, sentence-transformers, langchain splitters | Building RAG |
| `agents` | langgraph, pydantic-ai | Agent frameworks |
| `eval` | arize-phoenix, langsmith | Tracing + evaluation |
| `api` | fastapi, uvicorn, httpx | Serving a web API |
| `jupyter` | jupyter, ipykernel | Notebooks |
| `dev` | pytest, ruff, mypy, pre-commit | Development |
| `all` | everything above | Kitchen sink |

## Project layout

```
ai-project-template/
  src/
    core/          # config (pydantic-settings), logging, utils
    ml/            # classical ML + DL: dataset, features, train, predict
    rag/           # chunking, indexing, retrieval
    agents/        # LLM-driven loops (plan -> tool-call -> observe)
    workflows/     # deterministic LLM pipelines (chaining, routing)
    tools/         # stateless callables agents invoke
    prompts/       # versioned templates + registry
    evals/         # datasets/, offline/, judges/
    guardrails/    # input/output filters around LLM calls
    observability/ # OTel tracing, cost tracking, feedback
    services/      # business logic, DB, external APIs
    api/           # FastAPI entrypoint + routers
  tests/           # unit/ + integration/
  notebooks/       # numbered exploratory notebooks
  data/            # raw/ interim/ processed/ external/
  models/          # trained artifacts (gitignored)
  Dockerfile       # uv-based image serving the FastAPI app
  docker-compose.yml  # api + notebook services
  AGENTS.md        # canonical spec for coding agents
  CLAUDE.md        # points at AGENTS.md (Claude Code)
  pyproject.toml   # deps, ruff, pytest, mypy
  Makefile         # uv-based command interface
```

## The three-bucket rule

The most common confusion in AI projects is **where does X go?** This template enforces a clear split:

- **`agents/`** -- LLM loops. Decides what to do next.
- **`tools/`** -- stateless callables an agent invokes. Pure input → output.
- **`services/`** -- business logic, DB, external APIs. No LLM control flow.
- **`workflows/`** -- deterministic pipelines that call LLMs on a fixed path.

If you feel the urge to put an LLM loop in `services/`, stop and move it to `agents/`.

## Configuration

Single source of truth: [`src/core/config.py`](src/core/config.py). Loaded via `get_settings()` (cached). Override everything through environment variables -- see [`.env.example`](.env.example). Nested settings use `__` as delimiter: `LLM__MODEL=claude-sonnet-4-6` or the flat prefix form `LLM_MODEL=claude-sonnet-4-6`.

## Evaluation

Golden dataset lives in [`src/evals/datasets/golden.jsonl`](src/evals/datasets/golden.jsonl). Offline runners in [`src/evals/offline/`](src/evals/offline/). Judges (exact match, LLM-as-judge) in [`src/evals/judges/`](src/evals/judges/). Graduate to a managed registry (MLflow / LangSmith / Langfuse) when you scale.

## Observability

`src/observability/` wraps:
- **Tracing** -- OpenTelemetry, backend-agnostic (Phoenix, LangSmith, MLflow Tracing).
- **Cost tracking** -- aggregate LLM spend per run and per model.
- **Feedback** -- capture thumbs-up/down from users for online evals.

Call `setup_tracing()` once at app boot. Don't scatter instrumentation across business logic.

## Data management

- `data/raw/` is **immutable**. Never modify it.
- Derived artifacts go to `data/interim/` or `data/processed/`.
- Large data belongs outside the repo (DVC, S3). Pre-commit blocks files >5MB.

## Tooling

- **uv** for deps and commands. Everything goes through `uv run ...`.
- **Ruff** (line 120, py313, rules `E F W I UP B SIM`) for lint + format.
- **pytest** with async auto-mode and `pytest-cov`.
- **mypy** configured; not enforced in CI yet.
- **pre-commit** with ruff + large-file / merge-conflict hooks.

## License

MIT -- see [LICENSE](LICENSE).
