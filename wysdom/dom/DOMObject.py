from __future__ import annotations

from typing import Any, Optional, Iterator, Dict

from collections.abc import Mapping, MutableMapping

from ..exceptions import ValidationError
from ..base_schema import SchemaAnything

from .DOMElement import DOMElement
from . import DOMInfo
from .DOMProperties import DOMProperties
from .functions import document, schema


class DOMObject(DOMElement, MutableMapping):
    """
    An object with named properties.
    """

    __json_schema_properties__: DOMProperties = None
    __json_element_data__: Dict[str, Optional[DOMElement]] = None

    def __init__(
            self,
            value: Mapping[str, Any] = None,
            json_dom_info: DOMInfo = None
    ) -> None:
        """
        :param value:         A dict (or any :class:`collections.abc.Mapping`) containing the data to populate this
                              object's properties.
        :param json_dom_info: A :class:`~wysdom.dom.DOMInfo` named tuple containing information about this object's
                              position in the DOM.
        """
        if value and not isinstance(value, Mapping):
            raise ValidationError(
                f"Cannot validate input. Object is not a mapping: {value}"
            )
        schema(self).validate(value)
        super().__init__(None, json_dom_info)
        self.__json_element_data__ = {}
        try:
            for key, value in value.items():
                self[key] = value
        except KeyError as e:
            raise ValidationError(str(e))

    def __getitem__(self, key: str) -> Optional[DOMElement]:
        return self.__json_element_data__[key]

    def __setitem__(self, key: str, value: Optional[DOMElement]) -> None:
        if value is None:
            if key in self.__json_schema_properties__.required:
                raise ValueError(
                    f"The property '{key}' is not optional and cannot be None."
                )
            self.__json_element_data__[key] = None
        else:
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
        yield self.__json_dom_info__
        for key, value in self.items():
            if isinstance(value, DOMElement):
                yield from value.walk_elements()
            else:
                yield DOMInfo(value, document(self), self, key)

    def to_builtin(self) -> Dict[str, Any]:
        """
        Returns the contents of this DOM object as a Python builtin.

        :return: A Python dict containing this object's data
        """
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
        result = cls.__new__(cls)
        super(DOMObject, result).__init__(json_dom_info=self.__json_dom_info__)
        result.__json_element_data__ = dict(self.__json_element_data__)
        return result

    def __deepcopy__(self, memo: Dict[int, DOMElement]) -> DOMObject:
        cls = self.__class__
        result = cls(
            value=self.to_builtin(),
            json_dom_info=self.__json_dom_info__
        )
        memo[id(self)] = result
        return result
