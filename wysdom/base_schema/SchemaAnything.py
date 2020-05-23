from typing import Any, Dict

from .Schema import Schema


class SchemaAnything(Schema):

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {}
