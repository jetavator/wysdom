from typing import Any, Type, Union

from ..dom import DOMInfo, DOMDict

from .SchemaObject import SchemaObject
from ..base_schema import Schema
from .resolve_arg_to_type import resolve_arg_to_schema


class SchemaDict(SchemaObject):

    def __init__(
            self,
            items: Union[Type, Schema]
    ) -> None:
        super().__init__(
            additional_properties=resolve_arg_to_schema(items)
        )

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        return DOMDict(
            value,
            dom_info,
            _item_type=self.additional_properties
        )
