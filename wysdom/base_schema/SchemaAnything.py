from typing import Any, Dict, Tuple

from .Schema import Schema


class SchemaAnything(Schema):

    @property
    def jsonschema_dict(self) -> Dict[str, Any]:
        return {}
