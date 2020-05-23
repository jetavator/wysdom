from __future__ import annotations

from typing import Type, Union

import inspect

from ..base_schema import Schema
from ..dom import DOMElement

from ..base_schema import SchemaPrimitive


def resolve_arg_to_schema(
        arg: Union[Type, Schema]
) -> Schema:
    """
    Resolve an argument of heterogeneous type to a `Schema` instance.

    :param arg: Argument to resolve to a Schema. Must be one of:
                A primitive Python type (str, int, bool, float)
                A subclass of `UserObject`
                An instance of `Schema`.
    :return:    A `Schema` instance corresponding to the supplied argument.
    """
    if inspect.isclass(arg):
        if issubclass(arg, DOMElement):
            return arg.__json_schema__()
        else:
            return SchemaPrimitive(arg)
    elif isinstance(arg, Schema):
        return arg
    else:
        raise TypeError(f"Unexpected object type: {type(arg)}")
