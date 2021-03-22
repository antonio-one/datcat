import json
from contextlib import suppress
from json.decoder import JSONDecodeError

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

from datcat.adapters import repository
from datcat.domain import model
from datcat.entrypoints.mappings import create as create_mappings
from datcat.settings import (  # CATALOGUE_DEBUG,; CATALOGUE_HOST,; CATALOGUE_PORT,
    MAPPINGS_FILEPATH,
    SCHEMAS_PATH,
)

SCHEMA_REPOSITORY = repository.SchemaRepository()
MAPPINGS_REPOSITORY = repository.MappingsRepository()
ROOT = "/v1/datcat"

app = FastAPI(
    title="datcat",
    description="A simple data catalogue for GCP based event ingestion",
    version="0.1.3",
)


def json_response(response):
    response = jsonable_encoder(response)
    return JSONResponse(content=response)


def refresh_repository(repository_type: str) -> None:

    if repository_type == "schema":
        global SCHEMA_REPOSITORY
        SCHEMA_REPOSITORY.load(SCHEMAS_PATH)
    elif repository_type == "mappings":
        create_mappings()
        global MAPPINGS_REPOSITORY
        MAPPINGS_REPOSITORY.load(MAPPINGS_FILEPATH)
    else:
        raise Warning(f"Invalid {repository_type=}")


@app.get("/")
async def default():
    return RedirectResponse("/docs", status_code=302)


@app.get("/{ROOT:path}/schemas/list")
@app.get("/{ROOT:path}/schemas/list/refresh/{refresh}")
def list_catalogue(refresh: bool = False):

    if refresh:
        SCHEMA_REPOSITORY.load()
        # refresh_repository(repository_type="schema")

    response = SCHEMA_REPOSITORY.list_all()

    if response is None:
        return status.HTTP_404_NOT_FOUND

    return json_response(response)


@app.get("/{ROOT:path}/schemas/get/{schema_name}/version/{version}/refresh/{refresh}")
def search_schema_by_key(schema_name: str, version: int, refresh: bool):
    sf = model.SchemaFormat(
        schema_name=schema_name, schema_version=version, refresh=refresh
    )

    if refresh:
        refresh_repository(repository_type="schema")

    response = SCHEMA_REPOSITORY.get(sf.schema_name_version)

    if response is None:
        return status.HTTP_404_NOT_FOUND

    return json_response(response)


@app.get("/{ROOT:path}/mappings/list/refresh/{refresh}")
def list_mappings(refresh: bool):

    if refresh:
        refresh_repository(repository_type="mapping")

    response = MAPPINGS_REPOSITORY.list_all()

    if response is None:
        return status.HTTP_404_NOT_FOUND

    return json_response(response)


@app.get("/{ROOT:path}/mappings/get/{schema_name_version}/refresh/{refresh}")
def search_mapping_by_key(schema_name_version: str, refresh: bool):

    if refresh:
        refresh_repository(repository_type="mapping")

    response = MAPPINGS_REPOSITORY.get(key=schema_name_version)

    if response is None:
        return status.HTTP_404_NOT_FOUND

    return json_response(response)


@app.get("/{ROOT:path}/pii/list/refresh/{refresh}")
def list_pii_fields(refresh: bool):

    if refresh:
        refresh_repository(repository_type="schema")

    response = SCHEMA_REPOSITORY.list_all()

    if response is None:
        return status.HTTP_404_NOT_FOUND

    pii_fields = dict()
    for schema_name, fields in response.items():
        pii_fields[schema_name] = [
            field["name"] for field in fields if is_pii(field["description"])
        ]

    return json_response(pii_fields)


def is_pii(field_description: str):
    with suppress(JSONDecodeError):
        field_description = json.loads(field_description)
        field_description = field_description.get("pii", False)
        return field_description
