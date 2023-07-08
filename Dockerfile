FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi --no-root --no-dev

COPY . /app

#CMD [ "python", "main.py"]
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
