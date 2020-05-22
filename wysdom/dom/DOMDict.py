from __future__ import annotations

from typing import Generic, TypeVar, Optional, Any, Dict

from collections.abc import Mapping

from copy import deepcopy

from ..base_schema import Schema, SchemaAnything
from .DOMElement import DOMElement
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

    def __deepcopy__(self, memo: Dict[int, DOMElement]) -> DOMDict:
        cls = self.__class__
        # noinspection PyArgumentList
        result = cls(
            value={
                k: deepcopy(v, memo)
                for k, v in self.items()
            },
            json_dom_info=self.__json_dom_info__,
            _item_type=self.__json_schema_properties__.additional_properties
        )
        memo[id(self)] = result
        return result
