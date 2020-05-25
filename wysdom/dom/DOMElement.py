from __future__ import annotations

from typing import Any, Iterator, NamedTuple, Optional

from abc import ABC, abstractmethod

from ..base_schema import Schema, SchemaAnything


class DOMInfo(NamedTuple):
    """
    Named tuple containing information about a DOM element's position within the DOM.

    :param element:     The :class:`DOMElement` that this DOMInfo tuple provides information for.
    :param document:    The owning document for a :class:`DOMElement`, if it exists.
    :param parent:      The parent element of a :class:`DOMElement`, if it exists.
    :param element_key: The key of a particular :class:`DOMElement` in its parent element,
                        if it can be referred to by a key (i.e. if it its parent element
                        is a Mapping).
    """

    element: Optional[DOMElement] = None
    document: Optional[DOMElement] = None
    parent: Optional[DOMElement] = None
    element_key: Optional[str] = None


class DOMElement(ABC):
    """
    Abstract base class for any DOM element.
    """

    __json_dom_info__: DOMInfo = None

    @abstractmethod
    def __init__(
            self,
            value: Any = None,
            json_dom_info: DOMInfo = None,
            **kwargs: Any
    ) -> None:
        """
        :param value:         A data structure containing the data to populate this element.
        :param json_dom_info: A :class:`~wysdom.dom.DOMInfo` named tuple containing information about this object's
                              position in the DOM.
        :param kwargs:        Keyword arguments.
        """
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
        """
        Returns the contents of this DOM object as a Python builtin. Return type
        varies depending on the specific object type.
        """
        pass

    def walk_elements(self) -> Iterator[DOMInfo]:
        """
        Walk through the full tree structure within this DOM element.
        Returns an iterator of :class:`~wysdom.dom.DOMInfo` tuples in the form
        (element, document, parent element_key).

        :return: An iterator of :class:`~wysdom.dom.DOMInfo` tuples.
        """
        yield self.__json_dom_info__
