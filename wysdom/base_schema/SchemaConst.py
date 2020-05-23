from typing import Any, Dict

from .Schema import Schema


class SchemaConst(Schema):

    value: str = None

    def __init__(
            self,
            value: str
    ) -> None:
        self.value = value

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {
            "const": self.value
        }
