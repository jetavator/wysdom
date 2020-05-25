from typing import Dict, Union

from ..base_schema import Schema


class DOMProperties(object):
    """
    A container for property information for a :class:`.DOMObject`.
    """

    properties: Dict[str, Schema] = None
    additional_properties: Union[bool, Schema] = False

    def __init__(
            self,
            properties: Dict[str, Schema] = None,
            additional_properties: Union[bool, Schema] = False
    ) -> None:
        """
        :param properties:            A dictionary of :class:`~wysdom.base_schema.Schema.Schema` objects
                                      defining the expected names and types of a :class:`.DOMObject`'s
                                      properties.
        :param additional_properties: Defines whether a :class:`.DOMObject` permits additional
                                      dynamically-named properties. Can be True or False, or
                                      can be set to a specific `Schema` to restrict the permitted
                                      types of any additional properties.
        """
        self.properties = properties or {}
        self.additional_properties = additional_properties
