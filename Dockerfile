FROM python:3.10.1-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export --output requirements.txt --without-hashes --dev

FROM python:3.10.1-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN apt update \
    && apt install -y gcc \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
