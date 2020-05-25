from typing import Any, Dict

from .Schema import Schema


class SchemaAnything(Schema):
    """
    A schema where any valid JSON will be accepted.
    """

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {}
