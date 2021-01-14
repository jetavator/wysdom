from typing import Any, Dict, Tuple, Iterable, Optional

from ..dom import DOMInfo
from ..exceptions import ValidationError
from ..base_schema import Schema


class SchemaAnyOf(Schema):
    """
    A schema requiring a match with any of the permitted schemas supplied.

    :param allowed_schemas: A list (or other Iterable) containing the permitted
                            `Schema` objects.
    :param schema_ref_name: An optional unique reference name to use when this schema
                            is referred to by other schemas.
    """

    _allowed_schemas: Tuple[Schema] = None
    schema_ref_name: Optional[str] = None

    def __init__(
            self,
            allowed_schemas: Iterable[Schema],
            schema_ref_name: Optional[str] = None
    ) -> None:
        self._allowed_schemas = tuple(allowed_schemas)
        self.schema_ref_name = schema_ref_name

    def __call__(
            self,
            value: Any,
            dom_info: DOMInfo = None
    ) -> Any:
        valid_schemas = [
            allowed_schema
            for allowed_schema in self.allowed_schemas
            if allowed_schema.is_valid(value)
        ]
        if len(valid_schemas) > 1:
            raise ValidationError(
                "Ambiguous validation, more than one schema "
                f"is valid: {valid_schemas}"
            )
        if len(valid_schemas) == 0:
            raise ValidationError(
                f"No valid schema was found for the supplied value: {value}"
            )
        return valid_schemas[0](value, dom_info)

    @property
    def allowed_schemas(self) -> Tuple[Schema]:
        return self._allowed_schemas

    @property
    def referenced_schemas(self) -> Dict[str, Schema]:
        referenced_schemas = {}
        for allowed_schema in self.allowed_schemas:
            referenced_schemas.update(allowed_schema.referenced_schemas)
        if isinstance(self.schema_ref_name, str):
            referenced_schemas[self.schema_ref_name] = self
        return referenced_schemas

    @property
    def jsonschema_definition(self) -> Dict[str, Any]:
        return {
            'anyOf': [
                allowed_schema.jsonschema_ref_schema
                for allowed_schema in self.allowed_schemas
            ]
        }
