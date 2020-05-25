from typing import Optional

from ..base_schema import Schema
from .DOMElement import DOMElement
from . import DOMInfo


def dom(element: DOMElement) -> DOMInfo:
    """
    Retrieve a :class:`.DOMInfo` object for a :class:`.DOMElement` containing information
    about that element's position in the DOM.

    :param element: A DOM element
    :return:        The :class:`.DOMInfo` object for that DOM element
    """
    return element.__json_dom_info__


def document(element: DOMElement) -> Optional[DOMElement]:
    """
    Retrieve the owning document for a :class:`.DOMElement`, if it exists.

    :param element: A DOM element
    :return:        The owning document for that DOM element, or None if none exists
    """
    return dom(element).document


def parent(element: DOMElement) -> Optional[DOMElement]:
    """
    Retrieve the parent element of a :class:`.DOMElement`, if it exists.

    :param element: A DOM element
    :return:        The parent element of that DOM element, or None of none exists
    """
    return dom(element).parent


def key(element: DOMElement) -> Optional[str]:
    """
    Retrieve the key of a particular :class:`.DOMElement` in its parent element, if it can be
    referred to by a key (i.e. if it its parent element is a :class:`collections.abc.Mapping`).

    :param element: A DOM element
    :return:        The key of that DOM element in its parent, or None if it has no key
    """
    return dom(element).element_key


def schema(element: DOMElement) -> Schema:
    """
    Retrieve the :class:`~wysdom.base_schema.Schema` object for
    a particular :class:`.DOMElement`.

    :param element: A DOM element
    :return:        The :class:`~wysdom.base_schema.Schema` object associated
                    with that DOM element
    """
    return element.__json_schema__()
