from typing import Any, Dict, List, Tuple, Type
from enum import Enum

from .Schema import Schema


class SchemaEnum(Schema):
    """
    A schema requiring a one of a set of enumerated values.
    """

    enum: Type[Enum] = None

    def __init__(self, enum: Type[Enum]) -> None:
        self.enum = enum

    def __call__(self, value: Any, dom_info: Tuple = None) -> Any:
        validated_value = super().__call__(value)
        matched_enum_members = [
            member
            for member in self.enum.__members__.values()
            if member.value == validated_value
        ]
        if len(matched_enum_members) == 0:
            raise ValueError(f"Cannot find a member in {self.enum} with value {value}")
        if len(matched_enum_members) > 1:
            raise ValueError(
                f"Multiple ambiguous members in {self.enum} with value {value}"
            )
        return matched_enum_members[0]

    @property
    def allowed_values(self) -> List[Any]:
        return [member.value for member in self.enum.__members__.values()]

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {"enum": self.allowed_values}
