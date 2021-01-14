from __future__ import annotations

from typing import Any, Type, Iterator, Union, Mapping, List

import inspect

from ..mixins import RegistersSubclasses
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


class SchemaAnyRegisteredSubclass(SchemaAnyOf):
    """
    A SchemaAnyOf that allows any registered subclass of a UserObject.
    Exists so that allowed_schemas can be populated dynamically and is not fixed
    based on the object's current subclasses, but will also include any
    future subclasses that are defined after this object's creation.

    :param object_type:   The UserObject subclass.
    """

    def __init__(
            self,
            object_type: Type[UserObject]
    ):
        super().__init__(
            allowed_schemas=[],
            schema_ref_name=f"{object_type.__module__}.{object_type.__name__}"
        )
        assert issubclass(object_type, RegistersSubclasses)
        self.object_type = object_type

    @property
    def allowed_schemas(self) -> List[Schema]:
        return [
            subclass.__json_schema__()
            for subclass_list in self.object_type.registered_subclasses().values()
            for subclass in subclass_list
            if issubclass(subclass, UserObject)
            and not isinstance(subclass.__json_schema__(), SchemaAnyOf)
        ]


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
        has_subclasses = False
        if issubclass(cls, RegistersSubclasses):
            if cls.registered_subclasses():
                has_subclasses = True
        if has_subclasses:
            return SchemaAnyRegisteredSubclass(cls)
        else:
            return SchemaObject(
                properties=cls.__json_schema_properties__.properties,
                required=cls.__json_schema_properties__.required,
                additional_properties=cls.__json_schema_properties__.additional_properties,
                object_type=cls,
                schema_ref_name=f"{cls.__module__}.{cls.__name__}"
            )


