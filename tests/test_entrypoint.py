import json
import os
import pathlib
from glob import glob

from datcat.domain import model


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
