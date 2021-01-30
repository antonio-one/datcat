import abc
import json
import os
import typing
from glob import glob

from domain import model


class AbstractSchemaRepository:
    @abc.abstractmethod
    def add(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def list_all(self, *args):
        raise NotImplementedError

    @abc.abstractmethod
    def load(self, *args):
        raise NotImplementedError


class SchemaRepository(AbstractSchemaRepository):
    # TODO: figure out whether we can have db persistence
    def __init__(self):
        self.in_memory_schema_repository: model.SchemaRepo = {}

    def add(
        self, schema_key: model.SchemaKey, schema_definition: model.SchemaDefinition
    ) -> None:
        self.in_memory_schema_repository[schema_key] = schema_definition

    def get(self, schema_key: model.SchemaKey) -> model.SchemaDefinition:
        return self.in_memory_schema_repository.get(schema_key)

    def list_all(self) -> model.SchemaRepo:
        return self.in_memory_schema_repository

    def load(self, schemas_path: str) -> None:
        for schema_name in glob(f"{schemas_path}/*.json"):
            schema_path = os.path.join(schemas_path, schema_name)
            schema_name = os.path.basename(schema_path).partition(".")[0]
            with open(schema_path, "r") as sp:
                self.add(schema_name, self._validated_json(sp.read()))

    @staticmethod
    def _validated_json(payload: typing.Union[str, bytes]):
        # output = []
        try:
            output = json.loads(payload)
        except json.JSONDecodeError as jde:
            output = [{"JSONDecodeError": f"{jde}"}]
        return output

