# Changelog

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
