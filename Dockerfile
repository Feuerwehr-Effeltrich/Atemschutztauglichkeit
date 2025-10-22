FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

ADD . /app

RUN uv sync --locked

CMD ["uv", "run", "fastapi", "run", "src/main.py"]
