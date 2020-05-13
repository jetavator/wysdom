from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from jsonschema.validators import validator_for


class Schema(ABC):

    @abstractmethod
    def __call__(
            self,
            value: Any,
            dom_info: Tuple = None
    ) -> Any:
        return value

    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        return {}

    def is_valid(self, value: Any) -> bool:
        return validator_for(self.schema)(self.schema).is_valid(value)
