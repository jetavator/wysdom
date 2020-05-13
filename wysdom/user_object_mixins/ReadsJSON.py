from __future__ import annotations

import json

from ..dom import DOMObject


class ReadsJSON(DOMObject):

    def to_json(self) -> str:
        return json.JSONEncoder().encode(self.to_builtin())

    @classmethod
    def from_json(
            cls,
            json_string: str
    ) -> ReadsJSON:
        new_object = cls(
            json.JSONDecoder().decode(json_string)
        )
        return new_object

    @classmethod
    def from_json_file(cls, filename: str) -> ReadsJSON:
        with open(filename) as json_file:
            return cls(json.load(json_file))
