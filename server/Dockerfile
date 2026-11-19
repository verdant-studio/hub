FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Install dependencies first so this layer is cached across code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .

# Accept build-time argument
ARG CLIENT_URL

# Make it available as an env var
ENV CLIENT_URL=${CLIENT_URL}

EXPOSE 2000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--workers", "1", "--bind", "0.0.0.0:2000"]
