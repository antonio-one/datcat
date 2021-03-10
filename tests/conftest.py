import typing
from os import getenv

import pytest
from fastapi.testclient import TestClient

from datcat.adapters import repository
from datcat.entrypoints import flask_app
from datcat.entrypoints.app import app


@pytest.fixture(scope="session")
def schemas_path():
    return getenv("SCHEMAS_PATH")


@pytest.fixture(scope="session")
def schema_repository(schemas_path) -> typing.Dict:
    sr = repository.SchemaRepository()
    sr.load(schemas_path)
    return sr.in_memory_schema_repository


@pytest.fixture(scope="session")
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def test_client():
    return TestClient(app)
