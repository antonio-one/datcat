import json
import os
import pathlib
from glob import glob

import pytest

from datcat.domain import model


@pytest.mark.v0
def test_retrieve_schema_from_api(client, schemas_path):
    response = client.get(
        "schemas/search_by_key",
        query_string={
            "schema_class_name": "schema_one",
            "schema_version": "1",
            "refresh": "True",
        },
    )
    assert response.status_code == 200

    schema_name = "schema_one_v1"
    schema_path = pathlib.Path(schemas_path) / f"{schema_name}.json"
    with open(schema_path, "r") as sp:
        actual = json.loads(response.data)
        expected = json.loads(sp.read())
        assert actual == expected


@pytest.mark.v0
def test_retrieve_no_content_from_api(client):
    response = client.get(
        "/schemas/search_by_key",
        query_string={
            "schema_class_name": "unknown",
            "schema_version": "0",
            "refresh": "True",
        },
    )
    assert response.status_code == 204


@pytest.mark.v0
def test_list_all_from_api(client, schemas_path):

    response = client.get("/schemas", query_string={"refresh": "True"})
    actual_schemas = json.loads(response.data)
    assert response.status_code == 200

    expected_schemas: model.SchemaRepo = {}
    for file_path in glob(f"{schemas_path}/*.json"):
        schema_name = os.path.basename(os.path.splitext(file_path)[0])
        with open(file_path, "r") as fp:
            expected_schemas[schema_name] = json.loads(fp.read())

    assert actual_schemas == expected_schemas


@pytest.mark.v1
def test_default(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


@pytest.mark.v1
def test_retrieve_schema_from_api_v1(test_client, schemas_path):
    response = test_client.get(
        "/v1/datcat/schemas/get/schema_one/version/1/refresh/true"
    )
    assert response.status_code == 200

    schema_name = "schema_one_v1"
    schema_path = pathlib.Path(schemas_path) / f"{schema_name}.json"
    with open(schema_path, "r") as sp:
        actual = response.json()
        expected = json.loads(sp.read())
        assert actual == expected


@pytest.mark.v1
@pytest.mark.parametrize(
    "schema_name, schema_version, expected_status, expected_text",
    [
        ("non_existing_schema", 1, 200, 404),
        ("schema_one", 3, 200, 404),
        (
            "schema_one",
            "unexpected_string",
            422,
            {
                "detail": [
                    {
                        "loc": ["path", "version"],
                        "msg": "value is not a valid integer",
                        "type": "type_error.integer",
                    }
                ]
            },
        ),
        (101, 1, 200, 404),
        ("schema_two", -1, 200, 404),
        ("schema_two", 0, 200, 404),
    ],
)
def test_retrieve_no_content_from_api_v1(
    test_client, schema_name, schema_version, expected_status, expected_text
):
    url = f"/v1/datcat/schemas/get/{schema_name}/version/{schema_version}/refresh/true"
    response = test_client.get(url)

    assert response.status_code == expected_status
    assert response.json() == expected_text


@pytest.mark.v1
def test_list_all_from_api_v1(test_client, schemas_path):
    url = "/v1/datcat/schemas/list/refresh/true"
    response = test_client.get(url)
    actual_schemas = response.json()
    assert response.status_code == 200

    expected_schemas: model.SchemaRepo = {}
    for file_path in glob(f"{schemas_path}/*.json"):
        schema_name = os.path.basename(os.path.splitext(file_path)[0])
        with open(file_path, "r") as fp:
            expected_schemas[schema_name] = json.loads(fp.read())
    assert actual_schemas == expected_schemas
