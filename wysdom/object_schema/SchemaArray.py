from typing import Any, Union, Type, Dict, Iterable

from ..dom import DOMInfo, DOMList
from ..base_schema import Schema

from .resolve_arg_to_type import resolve_arg_to_schema


class SchemaArray(Schema):
    """
    A schema specifying an array (corresponding to a Python list)

    :param items: The permitted data type or schema for the items of this array. Must
                  be one of:
                  A primitive Python type (str, int, bool, float)
                  A subclass of `UserObject`
                  An instance of `Schema`
    """

    items: Schema = None

    def __init__(
            self,
            items: Union[Type, Schema]
    ) -> None:
        self.items = resolve_arg_to_schema(items)

    def __call__(
            self,
            value: Iterable,
            dom_info: DOMInfo = None
    ) -> Any:
        return DOMList(
            value,
            dom_info,
            item_type=self.items
        )

    @property
    def referenced_schemas(self) -> Dict[str, Schema]:
        return self.items.referenced_schemas

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {
            "array": {
                "items": self.items.jsonschema_ref_schema
            }
        }
