from __future__ import annotations

from typing import Any, Optional, Type, Iterator, Union, Mapping, Dict

import inspect

from ..mixins import RegistersSubclasses, has_registered_subclasses
from ..base_schema import Schema
from ..object_schema import SchemaObject, SchemaAnyOf
from ..dom import (
    DOMObject,
    DOMProperties,
    DOMInfo
)

from .UserProperty import UserProperty


class UserProperties(DOMProperties):
    """
    A container for property information for a :class:`.UserObject` subclass.
    """

    def __init__(
            self,
            user_class: Type[UserObject],
            additional_properties: Union[bool, Schema] = False
    ):
        """
        :param user_class:            The subclass of :class:`.UserObject` to extract properties from.
                                      Properties will be extracted from the class's
                                      :class:`~wysdom.user_objects.UserProperty` descriptors.
        :param additional_properties: Defines whether a :class:`.DOMObject` permits additional
                                      dynamically-named properties. Can be True or False, or
                                      can be set to a specific :class:`~wysdom.base_schema.Schema`
                                      to restrict the permitted types of any additional properties.
        """
        self._user_class = user_class
        properties = {}
        required = set()
        for superclass in reversed(list(self._schema_superclasses())):
            for k, v in superclass.__dict__.items():
                if isinstance(v, UserProperty):
                    if not v.name:
                        v.name = k
                    properties[v.name] = v.schema_type
                    if not v.optional:
                        required.add(v.name)
        super().__init__(properties, required, additional_properties)

    def _schema_superclasses(self) -> Iterator[Type[UserObject]]:
        for superclass in inspect.getmro(self._user_class):
            if (
                    issubclass(superclass, UserObject)
                    and superclass is not UserObject
            ):
                yield superclass


class UserObjectSchema(Schema):
    """
    A Schema for a given UserObject, which may behave like a SchemaAnyOf if
    the UserObject has registered subclasses, or a SchemaObject if it
    does not.

    The exact behavior (determined by UserObjectSchema.inner_schema) is
    determined dynamically to ensure that the schema will include any
    future registered subclasses that are defined after the UserObject's
    creation.

    :param object_type:   The UserObject subclass.
    """

    def __init__(
            self,
            object_type: Type[UserObject]
    ):
        self.object_type = object_type

    @property
    def inner_schema(self) -> Schema:
        if has_registered_subclasses(self.object_type):
            assert issubclass(self.object_type, RegistersSubclasses)
            return SchemaAnyOf(
                allowed_schemas=[
                    subclass.__json_schema__()
                    for subclass_list in self.object_type.registered_subclasses().values()
                    for subclass in subclass_list
                    if issubclass(subclass, UserObject)
                    and not has_registered_subclasses(subclass)
                ],
                schema_ref_name=f"{self.object_type.__module__}.{self.object_type.__name__}"
            )
        else:
            return SchemaObject(
                properties=self.object_type.__json_schema_properties__.properties,
                required=self.object_type.__json_schema_properties__.required,
                additional_properties=self.object_type.__json_schema_properties__.additional_properties,
                object_type=self.object_type,
                schema_ref_name=f"{self.object_type.__module__}.{self.object_type.__name__}"
            )

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        return self.inner_schema.__call__(value, dom_info)

    @property
    def referenced_schemas(self) -> Dict[str, Schema]:
        return self.inner_schema.referenced_schemas

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return self.inner_schema.jsonschema_definition

    @property
    def schema_ref_name(self) -> Optional[str]:
        return self.inner_schema.schema_ref_name


class UserObject(DOMObject):
    """
    Base class for user-defined DOM objects.

    :param value:         A dict-like object to populate the underlying data
                          object's keys. May be provided alone or in conjunction
                          with keyword arguments.

    :param json_dom_info: A named tuple with parameters (element, document, parent,
                          element_key) which specify this object's position in a
                          larger document object model. This is only required if you
                          need to set these values when creating an object manually:
                          when objects are created as part of a DOM specification,
                          these values are populated automatically.

    :param kwargs:        Keyword arguments to be used to populate the underlying
                          data object's keys. May be provided alone or in
                          conjunction with `value`.
    """

    __json_schema_properties__: UserProperties = None

    def __init_subclass__(
            cls,
            *args: Any,
            additional_properties: Union[bool, Schema] = False,
            **kwargs: Any
    ) -> None:
        cls.__json_schema_properties__ = UserProperties(cls)
        super().__init_subclass__(*args, **kwargs)

    def __init__(
            self,
            value: Mapping[str, Any] = None,
            json_dom_info: DOMInfo = None,
            **kwargs: Any
    ) -> None:
        if json_dom_info:
            if not isinstance(json_dom_info, DOMInfo):
                raise TypeError(
                    "The name json_dom_info is a reserved parameter of "
                    "UserObject and must be of type "
                    f"DOMInfo, not {type(json_dom_info)}"
                )
        super().__init__({**(value or {}), **kwargs}, json_dom_info)

    @classmethod
    def __json_schema__(cls) -> Schema:
        return UserObjectSchema(cls)


