from __future__ import annotations

from abc import ABC

from typing import Type, Optional, Any, Dict, List


class RegistersSubclasses(ABC):
    """
    A mixin class that allows subclasses to be registered in the
    main class by a registered name, using the `register_as`
    parameter in the subclass declaration.
    """

    registered_name = None
    __registered_subclasses__: Optional[Dict[str, RegisteredSubclassList]] = None

    def __init_subclass__(
        cls,
        register_as: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init_subclass__(**kwargs)

        if cls.__registered_subclasses__ is None and RegistersSubclasses in cls.__bases__:
            cls.__registered_subclasses__ = {}

        name = register_as or f"{cls.__module__}.{cls.__name__}"
        if not isinstance(name, str):
            raise TypeError(
                f"Parameter register_as must be a string, not {type(register_as)}")

        cls.__registered_subclasses__.setdefault(name, [])
        if cls not in cls.__registered_subclasses__[name]:
            cls.__registered_subclasses__[name].append(cls)
        cls.registered_name = name

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @classmethod
    def registered_subclasses(cls) -> Dict[str, RegisteredSubclassList]:
        """
        Return all of the registered subclasses in this class's namespace.

        :return: A dictionary of subclasses, indexed by registered name.
        """
        return {
            name: cls.registered_subclasses_by_name(name)
            for name in cls.__registered_subclasses__.keys()
            if len(cls.registered_subclasses_by_name(name)) > 0
        }

    @classmethod
    def registered_subclasses_by_name(cls, name) -> RegisteredSubclassList:
        """
        Return all of the registered subclasses for a given name that are a
        proper subclass of this class.

        :param name: The registered name of the subclass, as defined in
                     `register_as` when the class was declared.
        :return:     A list of subclasses of the class from which this method was called.
        """
        return [
            subclass
            for subclass in cls.__registered_subclasses__.get(name, [])
            if issubclass(subclass, cls)
            and subclass is not cls
        ]

    @classmethod
    def registered_subclass(
            cls,
            name: str,
            return_common_superclass: bool = True
    ) -> Type[RegistersSubclasses]:
        """
        Return a registered subclass by name.

        :param name:                     The registered name of the subclass, as defined in
                                         `register_as` when the class was declared.
        :param return_common_superclass: Disambiguate multiple valid subclasses by returning
                                         the common superclass among them, if one exists.
                                         Defaults to True.
        :return:                         A subclass of the class from which this method was called.
        :raises KeyError:                If no matching subclass is found or if multiple ambiguous
                                         subclasses are found.
        """
        matched_subclasses = cls.registered_subclasses_by_name(name)
        if len(matched_subclasses) == 0:
            raise KeyError(
                f"The key '{name}' matches no proper subclasses of {cls}.")
        elif len(matched_subclasses) > 1:
            if return_common_superclass:
                for matched_subclass in matched_subclasses:
                    if all(
                            issubclass(other_subclass, matched_subclass)
                            for other_subclass in matched_subclasses
                    ):
                        return matched_subclass
            raise KeyError(
                f"""
                The key '{name}' is ambiguous as it matches multiple proper subclasses of {cls}:
                {matched_subclasses}
                """)
        return matched_subclasses[0]

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
        :return:       An instance of a subclass of the class from which this method was called.
        """
        return cls.registered_subclass(name)(*args, **kwargs)


RegisteredSubclassList = List[Type[RegistersSubclasses]]
