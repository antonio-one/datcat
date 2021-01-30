# stage 1
FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/datcat"

# stage 2
FROM python-base as dependency-base

RUN apt-get update; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y curl \
    build-essential

EXPOSE ${CATALOGUE_PORT}

# stage 3
FROM dependency-base as development-base

WORKDIR ${PYTHONPATH}/
ADD .env ./.env
ADD adapters/ ./adapters/
ADD dist/ ./dist/
ADD domain/ ./domain/
ADD entrypoints/ ./entrypoints/
ADD schemas/ ./schemas/
ADD settings.py ./settings.py
ADD .secrets/ ./.secrets/

RUN pip3 install $(find dist/ -name *whl)

ENTRYPOINT ["python", "entrypoints/flask_app.py"]
