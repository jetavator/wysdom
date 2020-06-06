from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Optional

import jsonschema
from jsonschema.validators import validator_for

from ..exceptions import ValidationError


class Schema(ABC):
    """
    Abstract base class for JSON schemas. Objects of type `Schema` can be used to generate
    jsonschema-compatible dictionaries, and to validate potential input data against those
    schemas.

    Objects of type `Schema` are also callable, and when called will create DOM objects or
    primitive Python object containing the data that is supplied to them.
    """

    def __call__(
            self,
            value: Any,
            dom_info: Tuple = None
    ) -> Any:
        """
        Return either a DOM object or primitive Python object containing the data
        supplied in `value`, if `value` is a valid instance of this schema.

        :param value:    The raw value for which to create an object
        :param dom_info: An optional tuple containing DOM information for the object, if relevant
        :return:         A DOM object or primitive Python object containing the data in `value`
        """
        if self.is_valid(value):
            return value
        else:
            raise ValidationError(
                f"The supplied value does not conform to this schema: {value}"
            )

    @property
    def schema_ref_name(self) -> Optional[str]:
        """
        A unique reference name to use when this schema is referred to by other schemas.
        If this returns a string, references to this schema will use the $ref keyword without
        replicating the full schema.
        If this property returns None, the full contents of the schema will be used.

        :return: A string with a unique reference name if defined, else None.
        """
        return None

    @property
    def referenced_schemas(self) -> Dict[str, Schema]:
        """
        A dict of named schemas (i.e. schemas with a defined `schema_ref_name`) that are
        referenced in this schema, including itself if applicable.

        :return: A dict of `Schema` objects indexed by their `schema_ref_name`.
        """
        return {}

    @property
    @abstractmethod
    def jsonschema_definition(self) -> Dict[str, Any]:
        """
        The underlying jsonschema-compatible schema definition for this schema.

        :return: A jsonschema-compatible dictionary.
        """
        pass

    @property
    def jsonschema_ref_schema(self) -> Dict[str, Any]:
        """
        The jsonschema definition to use when referring to this schema in another schema.
        If `schema_ref_name` is defined, this will be a reference using the "$ref" keyword.
        If `schema_ref_name` is None, the raw definition of the schema will be used.

        :return: A jsonschema-compatible dictionary.
        """
        if self.schema_ref_name:
            return {"$ref": f"#/definitions/{self.schema_ref_name}"}
        else:
            return self.jsonschema_definition

    @property
    def jsonschema_full_schema(self) -> Dict[str, Any]:
        """
        The jsonschema definition to use when using this schema as a standalone schema.

        :return: A jsonschema-compatible dictionary.
        """
        output_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "definitions": {
                k: v.jsonschema_definition
                for k, v in self.referenced_schemas.items()
            }
        }
        output_schema.update(self.jsonschema_ref_schema)
        return output_schema

    def validate(self, value: Any) -> None:
        """
        Determine whether a given object conforms to this schema, and throw an error if not.

        :param value: An object to test for validity against this schema
        """
        jsonschema.validate(value, self.jsonschema_full_schema)

    def is_valid(self, value: Any) -> bool:
        """
        Determine whether a given object conforms to this schema.

        :param value: An object to test for validity against this schema
        :return:      True if the object is valid, otherwise False
        """
        return validator_for(self.jsonschema_full_schema)(self.jsonschema_full_schema).is_valid(value)
