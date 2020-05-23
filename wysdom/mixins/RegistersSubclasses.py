from __future__ import annotations

from abc import ABC

from typing import Type, Optional, Any, Dict


class RegistersSubclasses(ABC):
    """
    A mixin class that allows subclasses to be registered in the
    main class by a registered name, using the `register_as`
    parameter in the subclass declaration.
    """

    registered_name = None
    __registered_subclasses__: Optional[Dict[str, Type[RegistersSubclasses]]] = None

    def __init_subclass__(
        cls,
        register_as: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init_subclass__(**kwargs)

        if cls.__registered_subclasses__ is None and RegistersSubclasses in cls.__bases__:
            cls.__registered_subclasses__ = {}

        key = register_as or f"{cls.__module__}.{cls.__name__}"
        if not isinstance(key, str):
            raise TypeError(
                f"Parameter register_as must be a string, not {type(register_as)}")
        if (
            key in cls.__registered_subclasses__
            and cls.__registered_subclasses__[key] is not cls
        ):
            raise ValueError(
                f"""
                Cannot register {cls} as {key}:
                Already used by {cls.__registered_subclasses__[key]}.
                """)
        cls.__registered_subclasses__[key] = cls
        cls.registered_name = key

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def registered_subclasses(cls) -> Dict[str, Type[RegistersSubclasses]]:
        """
        Return all of the registered subclasses in this class's namespace.

        :return: A dictionary of subclasses, indexed by registered name.
        """
        return {
            name: subclass
            for name, subclass in cls.__registered_subclasses__.items()
            if issubclass(subclass, cls)
            and subclass is not cls
        }

    @classmethod
    def registered_subclass(cls, name: str) -> Type[RegistersSubclasses]:
        """
        Return a registered subclass by name.

        :param name: The registered name of the subclass, as defined in
                     `register_as` when the class was declared.
        :return:     A subclass of the base class for the namespace.
        """
        if name not in cls.__registered_subclasses__:
            raise KeyError(
                f"Unknown registered subclass key: {name}")
        return cls.__registered_subclasses__[name]

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
