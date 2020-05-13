from typing import Any, Union, Type, Dict, Iterable

from ..dom import DOMInfo, DOMList
from ..base_schema import Schema

from .resolve_arg_to_type import resolve_arg_to_schema


class SchemaArray(Schema):

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
            _item_type=self.items
        )

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "array": {
                "items": self.items
            }
        }
