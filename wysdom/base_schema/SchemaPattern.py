from typing import Any, Dict, Tuple

import re

from .SchemaPrimitive import SchemaPrimitive


class SchemaPattern(SchemaPrimitive):
    """
    A schema requiring a match for a regex pattern.
    """

    pattern: str = None

    def __init__(self, pattern: str) -> None:
        super().__init__(python_type=str)
        self.pattern = pattern

    def __call__(self, value: str, dom_info: Tuple = None) -> Any:
        if not re.match(self.pattern, value):
            raise ValueError(
                f"Parameter value {value} does not match regex pattern {self.pattern}."
            )
        return super().__call__(value)

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {"type": self.type_name, "pattern": self.pattern}
