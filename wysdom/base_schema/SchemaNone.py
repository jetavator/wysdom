from typing import Any, Tuple

from .SchemaType import SchemaType


class SchemaNone(SchemaType):
    type_name: str = 'null'

