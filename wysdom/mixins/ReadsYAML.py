from __future__ import annotations

from typing import Any, Union, TextIO

import yaml

from ..dom import DOMObject


class ReadsYAML(DOMObject):
    """
    Adds YAML reading and writing functionality to a DOMObject.
    """

    def to_yaml(self, **kwargs: Any) -> str:
        """
        Serialize the DOM object to YAML.

        :param kwargs: Optional keyword arguments to pass to PyYAML's safe_dump method.
                       See parameters for Dumper in https://pyyaml.org/wiki/PyYAMLDocumentation
        :return:       The DOM object, serialized as a YAML string
        """
        return yaml.safe_dump(self.to_builtin(), **kwargs)

    @classmethod
    def from_yaml(
            cls,
            yaml_string: Union[str, TextIO]
    ) -> ReadsYAML:
        """
        Create a new DOM object by from a YAML string.

        :param yaml_string: YAML string to read
        :return:            New DOM object instance
        """
        return cls(yaml.safe_load(yaml_string))

    @classmethod
    def from_yaml_file(cls, filename: str) -> ReadsYAML:
        """
        Create a new DOM object from a file on disk.

        :param filename: File path on disk of YAML file
        :return:         New DOM object instance
        """
        with open(filename, "r") as stream:
            return cls.from_yaml(stream)

