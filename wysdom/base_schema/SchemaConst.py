from typing import Any, Dict, Tuple

from .Schema import Schema


class SchemaConst(Schema):

    value: str = None

    def __init__(
            self,
            value: str
    ) -> None:
        self.value = value

    def __call__(
            self,
            value: str,
            dom_info: Tuple = None
    ) -> Any:
        if value != self.value:
            raise ValueError(f"Value can only be '{self.value}'.")
        return self.value

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "const": self.value
        }
