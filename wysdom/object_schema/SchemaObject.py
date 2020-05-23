from typing import Optional, Dict, Type, Any, Union

from ..dom import DOMInfo
from ..base_schema import SchemaType
from ..base_schema import Schema


class SchemaObject(SchemaType):

    type_name: str = "object"
    properties: Optional[Dict[str, Schema]] = None
    additional_properties: Union[bool, Schema] = False
    schema_ref_name: Optional[str] = None

    def __init__(
            self,
            properties: Optional[Dict[str, Schema]] = None,
            additional_properties: Union[bool, Schema] = False,
            object_type: Type = dict,
            schema_ref_name: Optional[str] = None
    ) -> None:
        self.properties = properties or {}
        self.additional_properties = additional_properties
        self.object_type = object_type
        self.schema_ref_name = schema_ref_name

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        return self.object_type(value, dom_info)

    @property
    def referenced_schemas(self) -> Dict[str, Schema]:
        referenced_schemas = {}
        if isinstance(self.additional_properties, Schema):
            referenced_schemas.update(self.additional_properties.referenced_schemas)
        for schema in self.properties.values():
            referenced_schemas.update(schema.referenced_schemas)
        if isinstance(self.schema_ref_name, str):
            referenced_schemas[self.schema_ref_name] = self
        return referenced_schemas

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {
            **super().jsonschema_definition,
            'properties': {
                k: v.jsonschema_ref_schema
                for k, v in self.properties.items()
            },
            "additionalProperties": (
                self.additional_properties.jsonschema_ref_schema
                if isinstance(self.additional_properties, Schema)
                else self.additional_properties
            )
        }


