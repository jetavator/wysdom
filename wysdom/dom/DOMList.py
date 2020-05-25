from __future__ import annotations

from abc import abstractmethod

from collections.abc import MutableSequence

from typing import (
    Generic, TypeVar, Union, Optional, Any, Iterable,
    Dict, List, Iterator, overload
)

from ..base_schema import Schema
from ..exceptions import ValidationError

from .DOMElement import DOMElement
from . import DOMInfo
from .functions import document

T_co = TypeVar('T_co')


class DOMList(DOMElement, MutableSequence, Generic[T_co]):
    """
    An array element (corresponding to a Python list).
    """

    __json_element_data__: List[DOMElement] = None

    def __init__(
            self,
            value: Iterable,
            json_dom_info: Optional[DOMInfo] = None,
            item_type: Optional[Schema] = None
    ) -> None:
        """
        :param value:         A list (or any :class:`Typing.Iterable`) containing the data to populate this
                              object's items.
        :param json_dom_info: A :class:`~wysdom.dom.DOMInfo` named tuple containing information about this object's
                              position in the DOM.
        :param item_type:     A :class:`~wysdom.Schema` object specifying what constitutes a valid item in this array.
        """
        if value and not isinstance(value, Iterable):
            raise ValidationError(
                f"Cannot validate input. Object is not iterable: {value}"
            )
        super().__init__(None, json_dom_info)
        self.__json_element_data__ = []
        if item_type is not None:
            self.item_type = item_type
        self[:] = value

    @overload
    @abstractmethod
    def __getitem__(self, i: int) -> T_co: ...

    @overload
    @abstractmethod
    def __getitem__(self, s: slice) -> MutableSequence[T_co]: ...

    def __getitem__(self, i: Union[int, slice]) -> Union[T_co, MutableSequence[T_co]]:
        return self.__json_element_data__[i]

    @overload
    @abstractmethod
    def __setitem__(self, i: int, o: T_co) -> None: ...

    @overload
    @abstractmethod
    def __setitem__(self, s: slice, o: Iterable[T_co]) -> None: ...

    def __setitem__(self, i: Union[int, slice], o: Union[T_co, MutableSequence[T_co]]) -> None:
        if type(i) is int:
            self.__json_element_data__[i] = self._new_child_item(o)
        else:
            self.__json_element_data__[i] = (self._new_child_item(x) for x in o)

    def _new_child_item(self, item: Any) -> DOMElement:
        return self.item_type(
            item,
            DOMInfo(
                document=document(self),
                parent=self
            )
        )

    @overload
    @abstractmethod
    def __delitem__(self, i: int) -> None: ...

    @overload
    @abstractmethod
    def __delitem__(self, i: slice) -> None: ...

    def __delitem__(self, i: int) -> None:
        del self.__json_element_data__[i]

    def __len__(self) -> int:
        return len(self.__json_element_data__)

    def __repr__(self):
        return repr(self.__json_element_data__)

    def __str__(self):
        return str(self.__json_element_data__)

    def insert(self, index: int, item: Any) -> None:
        self.__json_element_data__.insert(index, self._new_child_item(item))

    def to_builtin(self) -> List[Any]:
        """
        Returns the contents of this DOM object as a Python builtin.

        :return: A Python list containing this object's data
        """
        return [
            (
                v.to_builtin()
                if isinstance(v, DOMElement)
                else v
            )
            for v in self
        ]

    def walk_elements(self) -> Iterator[DOMInfo]:
        yield self.__json_dom_info__
        for value in self:
            if isinstance(value, DOMElement):
                yield from value.walk_elements()
            else:
                yield DOMInfo(value, document(self), self, None)

    def __copy__(self) -> DOMList:
        cls = self.__class__
        return cls(list(self))

    def __deepcopy__(self, memo: Dict[int, DOMElement]) -> DOMList:
        cls = self.__class__
        result = cls(
            value=self.to_builtin(),
            json_dom_info=self.__json_dom_info__,
            _item_type=self.item_type
        )
        memo[id(self)] = result
        return result
