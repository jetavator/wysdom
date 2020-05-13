from typing import Dict, Union

from ..base_schema import Schema


class DOMProperties(object):

    properties: Dict[str, Schema] = None
    additional_properties: Union[bool, Schema] = False

    def __init__(
            self,
            properties: Dict[str, Schema] = None,
            additional_properties: Union[bool, Schema] = False
    ) -> None:
        self.properties = properties or {}
        self.additional_properties = additional_properties
