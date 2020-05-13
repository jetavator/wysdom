from __future__ import annotations

from typing import Type, Union

import inspect

from ..base_schema import Schema
from ..dom import DOMElement

from ..base_schema import SchemaPrimitive


def resolve_arg_to_schema(
        arg: Union[Type, Schema]
) -> Schema:
    if inspect.isclass(arg):
        if issubclass(arg, DOMElement):
            return arg.__json_schema__()
        else:
            return SchemaPrimitive(arg)
    elif isinstance(arg, Schema):
        return arg
    else:
        raise TypeError(f"Unexpected object type: {type(arg)}")
