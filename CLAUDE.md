# CLAUDE.md

> This file stacks on top of the workspace root at `C:\Code\GitHub\`:
> - Root [`CLAUDE.md`](../../CLAUDE.md) -- voice, rules, routing map, references, skills, slash commands, conventions.
> - Root [`MEMORY.md`](../../MEMORY.md) -- live facts across repos.
> - Root [`STATUS.md`](../../STATUS.md) -- live PR/CI/security dashboard.
> - [`.claude/resources/`](../../.claude/resources/README.md) -- deep reference for collaboration, workflow, git, OSS, debugging, voice.
>
> Read those first. The guidance below only adds **repo-specific context** -- it does not override anything in the root.


This file exists for Claude Code. **The canonical agent spec is [AGENTS.md](AGENTS.md)** — Claude Code should read it in full.

The two files intentionally mirror each other's content; `AGENTS.md` is the open cross-tool standard (Codex, Cursor, Gemini CLI, Aider, Windsurf, Jules, Devin), and this file preserves Claude Code's expected filename. If the two ever diverge, `AGENTS.md` wins.

See [AGENTS.md](AGENTS.md) for:
- Architecture (domain-separated `src/` layout)
- The three-bucket rule (`agents/` vs `tools/` vs `services/` vs `workflows/`)
- Core conventions (imports, config, logging, prompts, evals)
- Tooling (ruff, pytest, mypy, pre-commit)
- Where new capabilities go
- Verification protocol