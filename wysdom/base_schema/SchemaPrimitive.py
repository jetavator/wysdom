from typing import Dict, Type, Optional, Any, Tuple

from .SchemaType import SchemaType


class SchemaPrimitive(SchemaType):
    """
    A schema requiring a primitive variable type

    :param python_type: The primitive Python type expected by this schema
    """

    JSON_TYPES: Dict[Type, str] = {
        str: 'string',
        bool: 'boolean',
        int: 'integer',
        float: 'number'
    }

    python_type: Type = None

    def __init__(
            self,
            python_type: Optional[Type] = None
    ) -> None:
        self.python_type = python_type

    def __call__(
            self,
            value: Any,
            dom_info: Tuple = None
    ) -> Any:
        return super().__call__(self.python_type(value))

    @property
    def type_name(self) -> str:
        return self.JSON_TYPES[self.python_type]
