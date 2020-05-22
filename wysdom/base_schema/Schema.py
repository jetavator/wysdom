from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from ..exceptions import ValidationError
from jsonschema.validators import validator_for


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
    @abstractmethod
    def jsonschema_dict(self) -> Dict[str, Any]:
        """
        Compile this schema as a jsonschema-compatible dictionary.

        :return: A jsonschema-compatible dictionary
        """
        pass

    def is_valid(self, value: Any) -> bool:
        """
        Determine whether a given object conforms to this schema.

        :param value: An object to test for validity against this schema
        :return:      True if the object is valid, otherwise False
        """
        return validator_for(self.jsonschema_dict)(self.jsonschema_dict).is_valid(value)
