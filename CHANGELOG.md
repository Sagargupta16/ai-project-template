# Changelog

## [3.1.1] - 2026-10-24

### Security
- Close all 62 open Dependabot alerts with new `[tool.uv] constraint-dependencies` floors at each fixed version and a targeted re-lock (`uv lock -P certifi -P fastmcp-slim -P filelock -P nbconvert -P opentelemetry-api -P pillow -P setuptools -P virtualenv`):
  - `pillow` 12.3.0 -> 13.0.0 (41 alerts, 5 critical, listed under both `Pillow` and `pillow`; fixed 13.0.0). Comes in through `matplotlib` in the `ml` extra.
  - `certifi` 2026.7.22 -> 2026.10.23 (critical, emSign root CAs with compromised intermediate keys; fixed 2026.10.19).
  - `virtualenv` 21.14.5 -> 21.14.13 (12 alerts: 4 high, 5 medium, 3 low; fixed 21.14.7 and 21.14.9), through `pre-commit` in the `dev` extra.
  - `filelock` 3.32.0 -> 4.2.4 (high ReadWriteLock symlink overwrite and 2 low Windows lock issues; fixed 4.2.1).
  - `nbconvert` 7.17.1 -> 7.17.2 (high, path traversal in cell output filenames).
  - `fastmcp-slim` 4.1.0 -> 4.1.3 (2 medium, authorization skip and OAuth issuer binding; fixed 4.1.2).
  - `opentelemetry-api` 1.44.0 -> 1.45.1 (medium, unbounded tracestate parsing).
  - `setuptools` 83.0.0 -> 84.2.1 (low, Windows path escape in legacy wheel install; fixed 84.1.0), through `torch`.
- The re-lock moves the rest of the OpenTelemetry family with `opentelemetry-api` (1.45.1 / 0.66b1), and `logfire` 4.39.0 -> 5.3.0 (from `pydantic-ai`'s `logfire` extra), `openapi-pydantic` 0.5.1 -> 0.6.0 and `packaging` 26.2 -> 26.3 with them. Nothing in `src/` imports any of these.
- Not changed: the image's 31 Trivy OS findings (glibc `2.41-12+deb13u4`, gcc-14 `14.2.0-19`, zlib `1:1.3.dfsg+really1.3.1-1`) are still unfixed in Debian trixie, the newest base distroless ships. The 11 Trivy `gcp-service-account` hits are the anthropic SDK docstring text `{"type": "service_account"}` in `resources/beta/agents/` and `types/beta/`, not a key.

## [3.1.0] - 2026-10-16

### Security
- Close the advisories that opened after #61 merged, with floors at the fixed versions and a targeted re-lock (`uv lock -P jupyter-server -P mcp -P strawberry-graphql`):
  - `strawberry-graphql` 0.320.4 -> 0.332.0 (Dependabot high, fixed 0.326.1, and low, fixed 0.327.2). `arize-phoenix` 19 pins 0.320.4, so the `eval` extra moves to `arize-phoenix` 20.22.0, which brings `fastmcp-slim` 4.1.0, `mcp` 2.3.0 and `sqlalchemy` 2.1.4 with it. Nothing in `src/` imports any of them.
  - `mcp` 1.28.1 -> 2.3.0 (Dependabot medium, fixed 1.30.0).
  - `jupyter-server` 2.20.0 -> 2.21.1 (Trivy high CVE-2026-86049, fixed 2.21.0); the `jupyter` extra floor moves to `>=2.21.0`.
- Rebuild the `Dockerfile` as two stages. The builder copies `pyproject.toml` and `uv.lock` and runs `uv sync --locked --no-dev --no-install-project --no-build --extra ml --extra llm --extra api`, so the image gets exactly the locked versions, from wheels only, and no package setup script runs. Before, only `pyproject.toml` was copied, so every build re-resolved from scratch (SonarCloud docker:S8541 and docker:S8544 on both `uv sync` lines and the `uv run` CMD).
- The runtime base moves from `python:3.14-slim` to `gcr.io/distroless/cc-debian13:nonroot` with a uv-managed Python 3.14: no shell, apt, uv or pip, and it runs as uid 65532. On 2026-10-16 Trivy found 172 issues in `python:3.14-slim` alone (166 Debian packages, 164 with no fixed version, plus urllib3 2.7.0, msgpack 1.1.2 and setuptools 70.3.0 vendored in the base image's pip 26.2.1, not in the app venv) and 31 in the distroless base (23 medium, 8 low, none fixable).
- The builder deletes the pip bundled with the managed Python, which carries the same vendored urllib3, msgpack and setuptools. Nothing at runtime uses it.
- Pin the uv image to `0.13.1` instead of `latest`.
- `ci.yml` gets a top-level `permissions: contents: read`, and the shared `security-scan.yml` reusable workflow is pinned to commit `a90df0c` instead of `@main` (CodeQL actions/missing-workflow-permissions and actions/unpinned-tag).

### Changed
- `ci.yml` drops the shared `python-ci.yml`, which wraps ruff and pytest in `|| true` and ran here with `run-tests: false`, for an inline `Lint & Test` job: `uv sync --locked --no-build --extra dev --extra ml --extra api`, then `ruff check .`, `ruff format --check .`, `mypy src` and `pytest -q`. A failing gate now fails CI, and mypy is enforced. Every `uv run` step passes `--locked --no-build`, so a step can neither re-resolve nor run a build script (SonarCloud githubactions:S8541 and S8544).
- The container starts uvicorn from the venv in exec form instead of `uv run`, so nothing re-syncs at startup, and has a `HEALTHCHECK` on `GET /health`.
- The Docker workflow also runs on pull requests that change `uv.lock`, `.python-version` or `.dockerignore`, and now runs the built image until its `HEALTHCHECK` reports healthy and `GET /health` answers, so a broken runtime fails CI instead of only the build.
- `RandomForestClassifier` in `src/ml/train.py` sets `min_samples_leaf` and `max_features` explicitly, from new `ML_MIN_SAMPLES_LEAF` and `ML_MAX_FEATURES` settings that default to the scikit-learn 1.9.0 defaults (`1` and `"sqrt"`), so trained models do not change (SonarCloud python:S6973).

### Fixed
- `pyproject.toml` said version `0.3.1` while this changelog had reached 3.0.2. It now says `3.1.0`.
- The docker-compose `notebook` service ran `uv run jupyter` in an image that never installed the `jupyter` extra. It now builds a dedicated `notebook` Dockerfile stage (builder plus the `jupyter` extra), and CI builds that target and runs `jupyter --version`.

## [3.0.2] - 2026-09-21

### Security
- Add `[tool.uv] constraint-dependencies` floors for vulnerable transitive deps and re-lock:
  - `httpx2` 2.9.1 -> 2.13.0 (high streaming decompression amplification #103, high secure WebSocket traffic sent without TLS through SOCKS proxies #98, medium conflicting Content-Length and Transfer-Encoding #102, medium multipart part header injection #101, medium quadratic SSE line buffering #99)
  - `httpcore2` 2.9.1 -> 2.13.0 (high, secure WebSocket traffic sent without TLS through SOCKS proxies, Dependabot #100)
- Floors are set at the advisory minimums (`httpx2>=2.12.0`, `httpcore2>=2.10.0`) rather than the resolved version, matching the 3.0.1 entries, so a future re-resolve cannot slide back under a patched version.
- The re-lock also adds `httpx2-jsfetch` 1.0, gated behind `sys_platform == 'emscripten'`. It installs only on WASM targets, so the footprint on normal platforms is unchanged.

## [3.0.1] - 2026-09-02

### Security
- Add `[tool.uv] constraint-dependencies` floors for vulnerable transitive deps and re-lock:
  - `cryptography` 49.0.0 -> 50.0.1 (high, Bleichenbacher oracle in PKCS#7 EnvelopedData decryption, Dependabot #94)
  - `h2` 4.4.0 -> 4.4.1 (medium, duplicate Host header request smuggling, Dependabot #95)
  - `tornado` 6.5.7 -> 6.5.8 (medium multipart DoS #97, low `set_cookie` attribute injection #96)

## [3.0.0] - 2026-04-18

Major restructure for any AI workload (ML, DL, LLM, RAG, agents).

### Added
- Domain-separated `src/` layout: `core`, `ml`, `rag`, `agents`, `workflows`, `tools`, `prompts`, `evals`, `guardrails`, `observability`, `services`, `api`.
- `AGENTS.md` as canonical cross-tool agent spec (Codex, Cursor, Gemini CLI, Aider, Windsurf).
- `pydantic-settings` based config with nested sub-settings (`ml`, `llm`, `rag`, `observability`).
- Prompt registry with versioned templates in `src/prompts/templates/`.
- Offline eval runner + golden dataset in `src/evals/`.
- Guardrails module with input/output filters and PII redaction.
- Observability module: tracing setup, cost tracker, feedback capture.
- FastAPI entrypoint in `src/api/main.py` with lifespan for tracing setup.
- `uv` as the canonical package manager; Makefile switched to `uv run` commands.
- CI updated to use `astral-sh/setup-uv`; format-check enforced.

### Changed
- `src/modeling/` renamed to `src/ml/`; `src/config.py` → `src/core/config.py`.
- `requirements*.txt` removed; deps live in `pyproject.toml` extras (`ml`, `dl`, `llm`, `rag`, `agents`, `eval`, `api`, `jupyter`, `dev`, `all`).
- Base install is now lean (~4 packages); heavy deps are opt-in.
- `Config` dataclass → `Settings` pydantic model; loaded via `get_settings()`.
- `tests/` split into `unit/` and `integration/`.
- CLAUDE.md is now a thin pointer to AGENTS.md.

### Removed
- `requirements.txt` and `requirements-dev.txt` (replaced by `pyproject.toml` extras).
- `src/modeling/` directory (moved to `src/ml/`).

## [2.0.0] - 2026-03-14

- Fill skeleton with working code (config, dataset, features, train, predict)
- Add pyproject.toml, ruff, pre-commit, CI
- Expand requirements.txt with common ML dependencies

## [1.0.0] - 2025-08-22

- Initial AI project template structure (empty skeleton)
