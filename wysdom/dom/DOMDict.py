from __future__ import annotations

from typing import Generic, TypeVar, Optional, Any

from collections.abc import Mapping

from ..base_schema import Schema, SchemaAnything
from .DOMObject import DOMObject
from . import DOMInfo
from .DOMProperties import DOMProperties

T_co = TypeVar('T_co')


class DOMDict(DOMObject, Generic[T_co]):

    _additional_properties: Schema = None

    def __init__(
            self,
            value: Optional[Mapping[str, Any]] = None,
            json_dom_info: Optional[DOMInfo] = None,
            _item_type: Optional[Schema] = None
    ) -> None:
        self.__json_schema_properties__ = DOMProperties(
            additional_properties=(_item_type or SchemaAnything())
        )
        super().__init__(
            value or {},
            json_dom_info
        )

    def __getitem__(self, key: str) -> T_co:
        return super().__getitem__(key)
