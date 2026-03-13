FROM python:3.12.13-slim-bookworm@sha256:4c50375fc4b8ea5ca06ac9485186ccb50171c99390b0e9300c2bac871cc2dc3e

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-install-project --python 3.12

COPY app ./app
COPY configs ./configs
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
