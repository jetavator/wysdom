from __future__ import annotations

from abc import ABC

from typing import Type, Optional, Any, Dict

import inspect


class RegistersSubclasses(ABC):
    """
    A mixin class that allows subclasses to be registered in the
    main class by a registered name, using the `register_as`
    parameter in the subclass declaration.
    """

    registered_name = None
    _registration_namespace = None
    _registered_subclasses = {}

    def __init_subclass__(
        cls,
        register_as: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init_subclass__(**kwargs)

        cls._registration_namespace = cls._get_registration_namespace()

        registered_name = register_as or cls._get_class_namespace(cls)

        key = (cls.registration_namespace(), str(registered_name))
        if (
            key in cls._registered_subclasses
            and cls._registered_subclasses[key] is not cls
        ):
            raise ValueError(
                f"""
                Cannot register {cls} as {registered_name}:
                Already used by {cls._registered_subclasses[key]}.
                """)
        cls._registered_subclasses[key] = cls
        cls.registered_name = str(registered_name)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def registration_namespace(cls) -> str:
        """
        :return: The registration namespace for this class.
        """
        try:
            return cls._registration_namespace
        except AttributeError:
            raise AttributeError(
                "Cannot find attribute '_registration_namespace'. "
                "Has another class overridden __init_subclass__ "
                "without calling super().__init_subclass__?"
            )

    @classmethod
    def registered_subclasses(cls) -> Dict[str, Type[RegistersSubclasses]]:
        """
        Return all of the registered subclasses in this class's namespace.

        :return: A dictionary of subclasses, indexed by registered name.
        """
        return {
            name: subclass
            for namespace, name, subclass in [
                (*key, subclass)
                for key, subclass in cls._registered_subclasses.items()
            ]
            if namespace == cls.registration_namespace()
            and issubclass(subclass, cls)
            and subclass is not cls
        }

    @classmethod
    def is_base_class(cls) -> bool:
        """
        Return True if this class is the base class for the namespace,
        i.e. the class that first declared RegisteredSubclasses as
        one of its bases.
        """
        return cls._get_class_namespace(cls) == cls.registration_namespace()

    @classmethod
    def registered_subclass(cls, name: str) -> Type[RegistersSubclasses]:
        """
        Return a registered subclass by name.

        :param name: The registered name of the subclass, as defined in
                     `register_as` when the class was declared.
        :return:     A subclass of the base class for the namespace.
        """
        key = (cls.registration_namespace(), name)
        if key not in cls._registered_subclasses:
            raise KeyError(
                f"Unknown registered subclass key: {name}")
        return cls._registered_subclasses[key]

    @classmethod
    def registered_subclass_instance(
        cls,
        name: str,
        *args: Any,
        **kwargs: Any
    ) -> RegistersSubclasses:
        """
        Create a new instance of a registered subclass by name.

        :param name:   The registered name of the subclass, as defined in
                       `register_as` when the class was declared.
        :param args:   Positional arguments to pass to the subclass.
        :param kwargs: Keyword arguments to pass to the subclass.
        :return:
        """
        return cls.registered_subclass(name)(*args, **kwargs)

    @classmethod
    def _get_registration_namespace(cls) -> str:
        return [
            cls._get_class_namespace(ancestor)
            for ancestor in inspect.getmro(cls)
            if RegistersSubclasses in ancestor.__bases__
        ][0]

    @staticmethod
    def _get_class_namespace(cls: type) -> str:
        return f"{cls.__module__}.{cls.__name__}"

