from typing import Optional, Dict, Type, Any, Union, Set

from ..dom import DOMInfo
from ..base_schema import SchemaType
from ..base_schema import Schema


class SchemaObject(SchemaType):
    """
    A schema specifying an object with named properties.

    :param properties:            A dictionary of `Schema` objects defining the expected
                                  names and types of this object's properties.
    :param additional_properties: Defines whether this object permits additional
                                  dynamically-named properties. Can be True or False, or
                                  can be set to a specific `Schema` to restrict the permitted
                                  types of any additional properties.
    :param object_type:           A custom object type to use when creating object instances
                                  from this schema.
    :param schema_ref_name:       An optional unique reference name to use when this schema
                                  is referred to by other schemas.
    """

    type_name: str = "object"
    properties: Optional[Dict[str, Schema]] = None
    required: Set[str] = None
    additional_properties: Union[bool, Schema] = False
    schema_ref_name: Optional[str] = None

    def __init__(
            self,
            properties: Optional[Dict[str, Schema]] = None,
            required: Set[str] = None,
            additional_properties: Union[bool, Schema] = False,
            object_type: Type = dict,
            schema_ref_name: Optional[str] = None
    ) -> None:
        self.properties = properties or {}
        self.required = required or set()
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
            "properties": {
                k: v.jsonschema_ref_schema
                for k, v in self.properties.items()
            },
            "required": list(sorted(self.required)),
            "additionalProperties": (
                self.additional_properties.jsonschema_ref_schema
                if isinstance(self.additional_properties, Schema)
                else self.additional_properties
            )
        }


