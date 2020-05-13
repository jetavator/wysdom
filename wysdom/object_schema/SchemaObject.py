from typing import Optional, Dict, Type, Any, Union

from ..dom import DOMInfo
from ..base_schema import SchemaType
from ..base_schema import Schema


class SchemaObject(SchemaType):

    type_name: str = "object"
    properties: Optional[Dict[str, Schema]] = None
    additional_properties: Union[bool, Schema] = False

    def __init__(
            self,
            properties: Optional[Dict[str, Schema]] = None,
            additional_properties: Union[bool, Schema] = False,
            object_type: Type = dict
    ) -> None:
        self.properties = properties or {}
        self.additional_properties = additional_properties
        self.object_type = object_type

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        return self.object_type(value, dom_info)

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            **super().schema,
            'properties': {
                k: v.schema
                for k, v in self.properties.items()
            },
            "additionalProperties": (
                self.additional_properties.schema
                if isinstance(self.additional_properties, Schema)
                else self.additional_properties
            )
        }


