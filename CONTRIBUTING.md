# Contributing to ai-project-template

This repo is a Python starter for ML, deep learning, LLM, RAG and agent projects. Bug reports, fixes, doc corrections and improvements that keep the template minimal are welcome: the base install stays lean and anything heavy goes behind an optional extra.

## Setup

You need Python 3.13 or newer (`requires-python = ">=3.13"`; `.python-version` pins 3.14) and [uv](https://docs.astral.sh/uv/). The `Makefile` is the command interface and everything runs through `uv`.

```bash
make setup                        # base install (uv sync)
uv sync --extra dev --extra ml    # enough for lint, format and the unit tests
make dev                          # every extra (uv sync --extra all)
make pre-commit                   # install the pre-commit hooks
```

## Before you open a PR

`.github/workflows/ci.yml` runs a `Lint & Test` job (`uv sync --locked --no-build --extra dev --extra ml --extra api`, then, each through `uv run --locked --no-build`, `ruff check .`, `ruff format --check .`, `mypy src` and `pytest -q`; any failure fails the build) and the shared security scan (Dependency Review on PRs plus a Trivy filesystem scan, pinned to a commit SHA). Separate workflows run CodeQL (`python` and `actions`, `security-extended` queries), Dependency Review (fails on high severity and on GPL-3.0 or AGPL-3.0 licenses), a TruffleHog secret scan, and a Docker build with a Trivy image scan when `Dockerfile`, `.dockerignore`, `.python-version`, `pyproject.toml`, `uv.lock` or `docker.yml` change.

Run these locally:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
make test
```

The pull request template also asks you to run the behavior, not only the checks: start `make api` and call the endpoint for API changes, and run `make eval` for eval changes. If you touch the `Dockerfile`, build it and check `GET /health` on the running container; the runtime stage is distroless (no shell, apt or uv), so build steps belong in the builder stage.

The pre-commit hooks run ruff (check with `--fix`, then format), whitespace and end-of-file fixers, YAML, TOML and JSON checks, a 5000 KB large-file limit, merge and case conflict checks, private-key detection, LF line endings and gitleaks.

## Conventions

These come from `AGENTS.md`, the canonical spec for this repo:

- Every `.py` file starts with `from __future__ import annotations`.
- Imports are absolute from the project root (`from src.core.config import get_settings`). No relative imports.
- Config lives only in `src/core/config.py` and is loaded with `get_settings()`. Override it with environment variables; nested settings use `__`.
- Logging: `logger = logging.getLogger(__name__)` and `%s`-style arguments, never f-strings in log calls.
- Three-bucket rule: `agents/` holds LLM loops, `tools/` holds stateless callables, `services/` holds business logic with no LLM control flow, `workflows/` holds fixed-path LLM pipelines. The table in `AGENTS.md` says where each new capability goes.
- Prompts are versioned (`<name>.v1.md`) and registered through `src.prompts.registry`.
- Dependencies go in `pyproject.toml` extras, never in a `requirements.txt`.
- Tests live in `tests/unit/` and `tests/integration/`. pytest-asyncio runs in auto mode, so async tests need no decorator.
- Ruff settings: line length 120, target py313, rules `E F W I UP B SIM`, double quotes.
- `data/raw/` is immutable. Do not commit `.env`, API keys, model weights or raw data.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`), with an optional scope such as `fix(deps):`.
- Add a `CHANGELOG.md` entry under a concrete next version, for example `## [3.1.1] - YYYY-MM-DD`, grouped under `Added`, `Changed`, `Fixed` or `Security`.
- Fill in the pull request template: type of change, affected domains and test plan.

## Security issues

Do not report vulnerabilities in public issues. Follow [SECURITY.md](SECURITY.md).

## License

This project is released under the MIT License (see [LICENSE](LICENSE)). By contributing, you agree that your contributions are licensed under it.
