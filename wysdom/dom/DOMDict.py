from __future__ import annotations

from typing import Generic, TypeVar, Optional, Any, Dict

from collections.abc import Mapping

from ..base_schema import Schema, SchemaAnything
from .DOMElement import DOMElement
from .DOMObject import DOMObject
from . import DOMInfo
from .DOMProperties import DOMProperties

T_co = TypeVar('T_co')


class DOMDict(DOMObject, Generic[T_co]):
    """
    An object with dynamic properties (corresponding to a Python dict).
    """

    def __init__(
            self,
            value: Optional[Mapping[str, Any]] = None,
            json_dom_info: Optional[DOMInfo] = None,
            item_type: Optional[Schema] = None
    ) -> None:
        """
        :param value:         A dict (or any :class:`collections.abc.Mapping`) containing the data to populate this
                              object's properties.
        :param json_dom_info: A :class:`~wysdom.dom.DOMInfo` named tuple containing information about this object's
                              position in the DOM.
        :param item_type:     A :class:`~wysdom.Schema` object specifying what constitutes a valid property
                              of this object.
        """
        self.__json_schema_properties__ = DOMProperties(
            additional_properties=(item_type or SchemaAnything())
        )
        super().__init__(
            value or {},
            json_dom_info
        )

    def __getitem__(self, key: str) -> T_co:
        return super().__getitem__(key)

    def __deepcopy__(self, memo: Dict[int, DOMElement]) -> DOMDict:
        cls = self.__class__
        result = cls(
            value=self.to_builtin(),
            json_dom_info=self.__json_dom_info__,
            _item_type=self.__json_schema_properties__.additional_properties
        )
        memo[id(self)] = result
        return result
