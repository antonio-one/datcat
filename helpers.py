import json
import typing
from adapters import repository
from domain.model import MappingFormat
from settings import SCHEMAS_PATH, MAPPINGS_FILEPATH
import logging


FORMAT = '%(asctime)s [%(levelname)s] %(module)s:%(funcName)s %(message)s'
logging.basicConfig(encoding='utf-8', level=logging.INFO, format=FORMAT)


def create_mappings():
    schema_repository = repository.SchemaRepository()
    schema_repository.load(schemas_path=SCHEMAS_PATH)
    repository_content = schema_repository.list_all()

    mappings: typing.Dict[str, typing.Dict] = {}

    for schema_name_version, _ in repository_content.items():
        cf = MappingFormat(schema_name_version=schema_name_version)
        mappings[cf.schema_name] = cf.mapping
        mappings[schema_name_version] = cf.mapping
        mappings[cf.topic_name] = cf.mapping
        mappings[cf.subscription_name] = cf.mapping

    with open(MAPPINGS_FILEPATH, "w") as mf:
        mf.write(json.dumps(mappings, indent=2))

    logging.info(f"{MAPPINGS_FILEPATH} (re)created.")