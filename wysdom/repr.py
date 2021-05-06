import inspect


def inspect_based_repr(object_to_repr: object):
    if not hasattr(object_to_repr, "__init__"):
        return object.__repr__(object_to_repr)
    arg_spec = inspect.getfullargspec(object_to_repr.__init__)
    if arg_spec.varargs or arg_spec.varkw:
        return object.__repr__(object_to_repr)
    arg_parts = [
        f"{arg}={repr(getattr(object_to_repr, arg))}"
        for arg in list(arg_spec.args[1:]) + list(arg_spec.kwonlyargs)
    ]
    return f"{object_to_repr.__class__.__name__}({', '.join(arg_parts)})"
