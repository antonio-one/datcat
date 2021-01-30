from flask import jsonify, redirect, request
from flask_api import FlaskAPI, status
from adapters import repository
from domain import model
from settings import CATALOGUE_DEBUG, CATALOGUE_HOST, CATALOGUE_PORT, SCHEMAS_PATH


SCHEMA_REPOSITORY = repository.SchemaRepository()

app = FlaskAPI(__name__)


def refresh_repository():
    global SCHEMA_REPOSITORY
    SCHEMA_REPOSITORY.load(SCHEMAS_PATH)


@app.route("/")
def default():
    return redirect("/list_catalogue?refresh=True", code=302)


@app.route("/search_by_key", methods=["GET"])
@app.route("/list_catalogue", methods=["GET"])
def list_catalogue():

    schema_name = request.args.get("schema_name", type=str)
    schema_version = request.args.get("schema_version", type=int)
    refresh = request.args.get("refresh", type=bool, default=False)
    sf = model.SchemaFormat(
        schema_name=schema_name, schema_version=schema_version, refresh=refresh
    )

    if refresh is True:
        refresh_repository()

    if schema_name is not None and schema_version is not None:
        response = SCHEMA_REPOSITORY.get(sf.schema_name_version)
    else:
        response = SCHEMA_REPOSITORY.list_all()

    if response is None:
        return "", status.HTTP_204_NO_CONTENT

    return jsonify(response)


def main():
    app.run(host=CATALOGUE_HOST, port=CATALOGUE_PORT, debug=CATALOGUE_DEBUG)


if __name__ == "__main__":
    main()
