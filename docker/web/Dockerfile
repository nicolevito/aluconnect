# docker/web/Dockerfile
FROM python:3.10-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev curl netcat postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt
RUN pip install pytest pytest-django pytest-cov
RUN pip install gunicorn

COPY ./docker/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./src /app

RUN mkdir -p /app/static

RUN useradd --create-home appuser
RUN chown -R appuser:appuser /app /entrypoint.sh
USER appuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
