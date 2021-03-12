from typing import Any, Type, Union, Optional

from ..dom import DOMInfo, DOMDict

from .SchemaObject import SchemaObject
from ..base_schema import Schema, SchemaPattern
from .resolve_arg_to_type import resolve_arg_to_schema


class SchemaDict(SchemaObject):
    """
    A schema specifying an object with dynamic properties (corresponding to a Python dict)

    :param items:       The permitted data type or schema for the properties of this object.
                        Must be one of:
                        A primitive Python type (str, int, bool, float)
                        A subclass of `UserObject`
                        An instance of `Schema`

    :param key_pattern: A regex pattern to validate the keys of the dictionary against.
    """

    def __init__(
            self,
            items: Union[Type, Schema],
            key_pattern: Optional[str] = None
    ) -> None:
        super().__init__(
            additional_properties=resolve_arg_to_schema(items),
            property_names=SchemaPattern(key_pattern)
        )

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        return DOMDict(
            value,
            dom_info,
            item_type=self.additional_properties
        )
