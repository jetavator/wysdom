from typing import Type, Any, Union, Optional, Callable

from ..base_schema import Schema
from ..object_schema import SchemaDict

from .UserProperty import UserProperty


class DictProperty(UserProperty):
    """
    A data descriptor for creating attributes in user-defined subclasses
    of :class:`~.wysdom.user_objects.UserObject` with a property_type
    of :class:`~.wysdom.object_schema.SchemaDict`.

    :param items:            The permitted data type or schema for the properties of the underlying
                             :class:`~.wysdom.object_schema.SchemaDict`. Must be one of:

                             A primitive Python type (str, int, bool, float)
                             A subclass of :class:`~.wysdom.user_objects.UserObject`.
                             An instance of :class:`~.wysdom.base_schema.Schema`.

    :param optional:         Determines whether this property is optional in the underlying
                             data object. If default or default_function are set, this
                             will default to True, otherwise False.

    :param name:             The name of this property in the underlying
                             data object. If not provided, this defaults to
                             the name of the attribute on the :class:`~.wysdom.user_objects.UserObject`
                             instance that owns the property.

    :param default:          A static value which provides a default value
                             for this property. Cannot be set in conjunction
                             with `default_function`.

    :param default_function: A function which provides a default value
                             for this property. The function must have a
                             single positional argument, `self`, which is
                             passed the :class:`~.wysdom.user_objects.UserObject` instance that
                             owns the property. Cannot be set in conjunction
                             with `default`.

    :param persist_defaults: If this property is set to True and a UserProperty has either the
                             `default` or `default_function` property, when the UserProperty returns
                             a default value that value will also be explicitly stored in the underlying
                             data object. This is often desirable behavior if the UserProperty
                             returns another object and your code expects it to return the same
                             object instance each time it is accessed.

    :param key_pattern:      A regex pattern to validate the keys of the dictionary against.
    """

    def __init__(
        self,
        items: Union[Type, Schema],
        optional: Optional[bool] = None,
        name: Optional[str] = None,
        default: Optional[Any] = None,
        default_function: Optional[Callable] = None,
        persist_defaults: Optional[bool] = None,
        key_pattern: Optional[str] = None,
    ) -> None:
        super().__init__(
            property_type=SchemaDict(items, key_pattern=key_pattern),
            optional=optional,
            name=name,
            default=default,
            default_function=default_function,
            persist_defaults=persist_defaults,
        )
