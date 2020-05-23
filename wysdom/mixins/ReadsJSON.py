from __future__ import annotations

import json

from ..dom import DOMObject


class ReadsJSON(DOMObject):
    """
    Adds JSON reading and writing functionality to a DOMObject.
    """

    def to_json(self) -> str:
        """
        Serialize the DOM object to JSON.

        return: The DOM object, serialized as a JSON string
        """
        return json.JSONEncoder().encode(self.to_builtin())

    @classmethod
    def from_json(
            cls,
            json_string: str
    ) -> ReadsJSON:
        """
        Create a new DOM object by from a JSON string.

        :param json_string: JSON string to read
        :return:            New DOM object instance
        """
        return cls(
            json.JSONDecoder().decode(json_string)
        )

    @classmethod
    def from_json_file(cls, filename: str) -> ReadsJSON:
        """
        Create a new DOM object from a file on disk.

        :param filename: File path on disk of JSON file
        :return:         New DOM object instance
        """
        with open(filename) as json_file:
            return cls(json.load(json_file))
