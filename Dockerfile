# stage 1
FROM python:3.8-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# stage 2
FROM python-base as dependency-base

RUN apt-get update; \
    apt-get install -y build-essential

EXPOSE ${CATALOGUE_PORT}

# stage 3
FROM dependency-base as development-base

WORKDIR /datcat/
ADD .env ./.env
ADD datcat/adapters/ ./adapters/
ADD dist/ ./dist/
ADD datcat/domain/ ./domain/
ADD datcat/entrypoints/ ./entrypoints/
ADD catalogue/ ./catalogue/
ADD settings.py ./settings.py

RUN pip3 install $(find dist/ -name *whl)

ENTRYPOINT ["python", "entrypoints/flask_app.py"]
