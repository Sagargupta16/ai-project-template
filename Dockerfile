# The builder installs the locked deps into a venv on a uv-managed Python; the
# runtime is distroless (no shell, no package manager, no uv) and ships only that
# Python, the venv and src/. The notebook stage is only for docker compose.

FROM debian:trixie-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

WORKDIR /app

# Python version comes from .python-version. The venv never uses the bundled
# pip, and its vendored urllib3, msgpack and setuptools carry CVEs, so drop it.
COPY .python-version ./
RUN uv python install
RUN rm -rf /python/cpython-*/lib/python3.*/site-packages/pip /python/cpython-*/lib/python3.*/site-packages/pip-*.dist-info

# Exactly what uv.lock pins, wheels only, so no package setup scripts run
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project --no-build --extra ml --extra llm --extra api

# Jupyter for the docker-compose `notebook` service (`target: notebook`).
# Kept before the runtime stage so a plain `docker build` still ends on distroless.
FROM builder AS notebook
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project --no-build --extra ml --extra llm --extra api --extra jupyter
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

FROM gcr.io/distroless/cc-debian13:nonroot

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=builder /python /python
COPY --from=builder /app/.venv /app/.venv
COPY src/ src/

USER nonroot
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"]

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
