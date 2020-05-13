from __future__ import annotations

from typing import Any, Iterator, Dict

from collections.abc import Mapping, MutableMapping

from copy import deepcopy

from wysdom.mixins import RegistersSubclasses

from ..exceptions import ValidationError
from ..base_schema import SchemaAnything

from .DOMElement import DOMElement
from . import DOMInfo
from .DOMProperties import DOMProperties
from .functions import document


class DOMObject(DOMElement, MutableMapping, RegistersSubclasses):

    __json_schema_properties__: DOMProperties = None
    __json_element_data__: Dict[str, DOMElement] = None

    def __init__(
            self,
            value: Mapping[str, Any] = None,
            json_dom_info: DOMInfo = None
    ) -> None:
        if value and not isinstance(value, Mapping):
            raise ValidationError(
                f"Cannot validate input. Object is not a mapping: {value}"
            )
        super().__init__(None, json_dom_info)
        self.__json_element_data__ = {}
        try:
            for key, value in value.items():
                self[key] = value
        except KeyError as e:
            raise ValidationError(str(e))

    def __getitem__(self, key: str) -> DOMElement:
        return self.__json_element_data__[key]

    def __setitem__(self, key: str, value: DOMElement) -> None:
        item_class = self.__json_schema_properties__.properties.get(
            key, self.__json_schema_properties__.additional_properties)
        if item_class is True:
            item_class = SchemaAnything()
        if not item_class:
            raise KeyError(
                f"No property named '{key}' exists, and "
                "additional properties are not allowed."
            )
        self.__json_element_data__[key] = item_class(
            value,
            DOMInfo(
                document=document(self),
                parent=self,
                element_key=key
            )
        )

    def __delitem__(self, key: str) -> None:
        del self.__json_element_data__[key]

    def __len__(self) -> int:
        return len(self.__json_element_data__)

    def __iter__(self) -> Iterator[str]:
        return iter(self.__json_element_data__)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.__json_element_data__)})"

    def __str__(self):
        return str(self.__json_element_data__)

    def walk_elements(self) -> Iterator[DOMInfo]:
        for key, value in self.items():
            if isinstance(value, DOMElement):
                yield from value.walk_elements()
            else:
                yield DOMInfo(value, document(self), self, key)

    def to_builtin(self) -> Dict[str, Any]:
        return {
            k: (
                v.to_builtin()
                if isinstance(v, DOMElement)
                else v
            )
            for k, v in self.items()
        }

    def __copy__(self) -> DOMObject:
        cls = self.__class__
        return cls(dict(self))

    def __deepcopy__(self, memo: Dict[int, DOMElement]) -> DOMObject:
        cls = self.__class__
        result = cls(deepcopy(dict(self), memo))
        memo[id(self)] = result
        return result
