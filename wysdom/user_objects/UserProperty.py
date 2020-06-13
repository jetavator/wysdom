from typing import Type, Any, Union, Optional, Callable

from ..base_schema import Schema
from ..object_schema import resolve_arg_to_schema
from ..dom import DOMObject, DOMInfo, document


class UserProperty(object):
    """
    A data descriptor for creating attributes in user-defined subclasses
    of :class:`~.wysdom.user_objects.UserObject` which are mapped to keys in the underlying
    data object and to the `properties` key in the object's JSON schema.

    :param property_type:    The data type or schema for this property. Must
                             be one of:

                             * A primitive Python type (:class:`str`, :class:`int`,
                               :class:`bool`, :class:`float`)
                             * A subclass of :class:`~.wysdom.user_objects.UserObject`
                             * An instance of :class:`~wysdom.base_schema.Schema`

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
    """

    def __init__(
            self,
            property_type: Union[Type, Schema],
            optional: Optional[bool] = None,
            name: Optional[str] = None,
            default: Optional[Any] = None,
            default_function: Optional[Callable] = None,
            persist_defaults: Optional[bool] = None
    ) -> None:
        if default is not None or default_function is not None:
            if default is not None and default_function is not None:
                raise ValueError("Cannot use both default and default_function.")
            if optional is False:
                raise ValueError(
                    "Cannot set optional to False if default or default_function are specified.")
            self.optional = True
        else:
            self.optional = bool(optional)
        self.schema_type = resolve_arg_to_schema(property_type)
        self.name = name
        self.default = default
        self.default_function = default_function
        self.persist_defaults = persist_defaults

    def __get__(
            self,
            instance: DOMObject,
            owner: Type[DOMObject]
    ) -> Any:
        if instance is None:
            raise AttributeError(
                "UserProperty is not valid as a class data descriptor")
        if self.name not in instance:
            if self.default_function:
                default_value = self.default_function(instance)
            else:
                default_value = self.default
            if self.persist_defaults:
                instance[self.name] = default_value
                return instance[self.name]
            elif default_value is None:
                return default_value
            else:
                return self.schema_type(
                    default_value,
                    DOMInfo(
                        document=document(instance),
                        parent=instance,
                        element_key=self.name
                    )
                )
        return instance[self.name]

    def __set__(
            self,
            instance: DOMObject,
            value: Any
    ) -> None:
        instance[self.name] = value
