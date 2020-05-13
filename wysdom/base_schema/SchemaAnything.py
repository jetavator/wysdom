from typing import Any, Dict, Tuple

from .Schema import Schema


class SchemaAnything(Schema):

    def __call__(
            self,
            value: Any,
            dom_info: Tuple = None
    ) -> Any:
        return value

    @property
    def schema(self) -> Dict[str, Any]:
        return {}
