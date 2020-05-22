from typing import Optional

from ..base_schema import Schema
from .DOMElement import DOMElement
from . import DOMInfo


def dom(element: DOMElement) -> DOMInfo:
    return element.__json_dom_info__


def document(element: DOMElement) -> Optional[DOMElement]:
    return dom(element).document


def parent(element: DOMElement) -> Optional[DOMElement]:
    return dom(element).parent


def key(element: DOMElement) -> Optional[str]:
    return dom(element).element_key


def schema(element: DOMElement) -> Schema:
    return element.__json_schema__()
