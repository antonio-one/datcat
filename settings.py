import typing

from decouple import config

SCHEMAS_PATH = config("SCHEMAS_PATH")
MAPPINGS_FILEPATH = config("MAPPINGS_FILEPATH")
CATALOGUE_SCHEME = config("CATALOGUE_SCHEME")
CATALOGUE_HOST = config("CATALOGUE_HOST")
CATALOGUE_PORT = config("CATALOGUE_PORT")
CATALOGUE_DEBUG = config("CATALOGUE_DEBUG")

SCHEMA_TOPIC_SUBSCRIPTION: typing.Dict[str, str]
SCHEMA_TOPIC_SUBSCRIPTION = {}
