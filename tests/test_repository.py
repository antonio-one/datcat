import json
import os


def test_schema_path_contains_only_json_files(schemas_path):
    filetypes = set()
    for f in os.listdir(schemas_path):
        filetypes.add(os.path.splitext(f)[1])
    assert filetypes == {".json"}


def test_schema_exists(schemas_path, schema_repository):
    schema_name = "schema_one_v1"
    schema_path = os.path.join(schemas_path, f"{schema_name}.json")
    with open(schema_path, "r") as sp:
        expected_schema_definition = json.loads(sp.read())
        assert schema_repository[schema_name] == expected_schema_definition


def test_schema_does_not_exist(schema_repository):
    schema_name = "schema_unknown_v1"
    assert schema_repository.get(schema_name) is None
