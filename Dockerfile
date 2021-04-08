# stage 1
FROM python:3.8-slim as os-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update; \
    apt-get install -y build-essential \
    procps \
    iputils-ping

EXPOSE ${CATALOGUE_PORT}

# stage 2
FROM os-base as app-base

ARG APPDIR=/datcat
WORKDIR ${APPDIR}/
COPY example_catalogue ./example_catalogue
COPY datcat ./datcat
COPY dist ./dist
RUN pip3 install ${APPDIR}/dist/*.whl

# stage 3
FROM app-base as main

CMD uvicorn datcat.entrypoints.app:app --host=0.0.0.0 --port=${CATALOGUE_PORT}
