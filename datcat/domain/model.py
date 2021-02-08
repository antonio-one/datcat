import typing
from urllib.parse import urlencode

BaseKey = typing.NewType("SchemaKey", str)
BaseValue = typing.NewType("BaseValue", str)
BaseField = typing.Dict[BaseKey, BaseValue]
BaseDefinition = typing.NewType("BaseDefinition", typing.List[BaseField])
BaseRepo = typing.NewType("BaseRepository", typing.Dict[BaseKey, BaseDefinition])

SchemaKey = BaseKey
SchemaValue = BaseValue
SchemaField = BaseField
SchemaDefinition = BaseDefinition
SchemaRepo = BaseRepo

MappingKey = BaseKey
MappingValue = BaseValue
MappingField = BaseField
MappingDefinition = BaseDefinition
MappingRepo = BaseRepo


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


class MappingFormat:
    def __init__(self, schema_name_version: str):
        self.schema_name_version = schema_name_version

    @property
    def schema_name(self) -> str:
        return self.schema_name_version.rpartition("_")[0]

    @property
    def topic_name(self) -> str:
        return f"{self.schema_name}_topic"

    @property
    def subscription_name(self):
        # TODO: There may be multiple subscriptions per topic
        return f"{self.schema_name}_subscription"

    @property
    def mapping(self):
        return {
            "schema_name": self.schema_name,
            "topic_name": self.topic_name,
            "subscription_name": self.subscription_name,
        }
