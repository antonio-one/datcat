import typing
from urllib.parse import urlencode

SchemaKey = typing.NewType("SchemaKey", str)
SchemaValue = typing.NewType("SchemaValue", typing.Any)
SchemaField = typing.Dict[SchemaKey, SchemaValue]
SchemaDefinition = typing.NewType("SchemaDefinition", typing.List[SchemaField])
SchemaRepo = typing.NewType("SchemaRepo", typing.Dict[SchemaKey, SchemaDefinition])


class SchemaFormat:
    def __init__(self, schema_name: str, schema_version: int, refresh: bool):
        self.schema_name = schema_name
        self.schema_version = schema_version
        self.refresh = refresh

    @property
    def schema_name_version(self) -> str:
        return f"{self.schema_name}_v{self.schema_version}"

    @property
    def params(self):
        output: typing.Dict[str, typing.Any]
        output = {
            "schema_name": self.schema_name,
            "schema_version": self.schema_version,
            "refresh": self.refresh,
        }
        return output

    @property
    def querystring(self) -> str:
        return urlencode(self.params)

