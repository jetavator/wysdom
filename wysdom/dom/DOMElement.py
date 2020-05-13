from __future__ import annotations

from typing import Any, Iterator, NamedTuple, Optional

from abc import ABC, abstractmethod

from ..base_schema import Schema, SchemaAnything


class DOMInfo(NamedTuple):

    element: Optional[DOMElement] = None
    document: Optional[DOMElement] = None
    parent: Optional[DOMElement] = None
    element_key: Optional[str] = None


class DOMElement(ABC):

    __json_dom_info__: DOMInfo = None

    @abstractmethod
    def __init__(
            self,
            value: Any = None,
            json_dom_info: DOMInfo = None,
            **kwargs: Any
    ) -> None:
        if value is not None:
            raise ValueError(
                "The parameter 'value' must be handled by a non-abstract subclass."
            )
        if json_dom_info:
            self.__json_dom_info__ = DOMInfo(
                element=self,
                document=(
                    self if json_dom_info.document is None
                    else json_dom_info.document
                ),
                parent=json_dom_info.parent,
                element_key=json_dom_info.element_key
            )
        else:
            self.__json_dom_info__ = DOMInfo(
                element=self, document=self)

    @classmethod
    def __json_schema__(cls) -> Schema:
        return SchemaAnything()

    @abstractmethod
    def to_builtin(self) -> Any:
        pass

    def walk_elements(self) -> Iterator[DOMInfo]:
        yield self.__json_dom_info__
