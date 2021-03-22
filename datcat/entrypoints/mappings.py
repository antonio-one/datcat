import json
import logging

from datcat.adapters import repository
from datcat.domain import model
from datcat.settings import MAPPINGS_FILEPATH, SCHEMAS_PATH

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)


def create_mappings():
    schema_repository = repository.SchemaRepository()
    schema_repository.load(schemas_path=SCHEMAS_PATH)
    repository_content = schema_repository.list_all()

    m_key: model.MappingKey = ""
    m_value: model.MappingValue = {}
    m_repo: model.MappingRepo = {}

    for schema_name_version, _ in repository_content.items():
        cf = model.MappingFormat(schema_name_version=schema_name_version)
        m_key = schema_name_version
        m_value = {
            "schema_name": cf.schema_name,
            "topic_name": cf.topic_name,
            "subscription_name": cf.subscription_name,
        }

        m_repo[m_key] = m_value

    with open(MAPPINGS_FILEPATH, "w") as mf:
        mf.write(json.dumps(m_repo, indent=2))

    logging.info(f"{MAPPINGS_FILEPATH} (re)created.")
