from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Any, Dict

from .Schema import Schema


class SchemaType(Schema, ABC):

    @property
    @abstractmethod
    def type_name(self) -> str:
        pass

    @property
    def schema(self) -> Dict[str, Any]:
        return {"type": self.type_name}


