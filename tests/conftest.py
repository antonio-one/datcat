import typing

import pytest
from adapters import repository
from entrypoints import flask_app

from os import getenv


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
