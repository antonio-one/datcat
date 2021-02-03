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

ARG WHEEL=datcat-0.1.3-py3-none-any.whl
ARG APPDIR=/datcat

WORKDIR ${APPDIR}/
ADD catalogue/ ./catalogue
ADD datcat/ ./
ADD dist/${WHEEL} ./
ADD .env ./

RUN pip3 install ${APPDIR}/${WHEEL}

ENTRYPOINT ["python", "entrypoints/flask_app.py"]
