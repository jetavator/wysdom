from __future__ import annotations

from typing import Any, Union, TextIO

import yaml

from ..dom import DOMObject


class ReadsYAML(DOMObject):

    def to_yaml(self, **kwargs: Any) -> str:
        return yaml.safe_dump(self.to_builtin(), **kwargs)

    @classmethod
    def from_yaml(
            cls,
            yaml_string: Union[str, TextIO]
    ) -> ReadsYAML:
        return cls(yaml.safe_load(yaml_string))

    @classmethod
    def from_yaml_file(cls, filename: str) -> ReadsYAML:
        with open(filename, "r") as stream:
            return cls.from_yaml(stream)

