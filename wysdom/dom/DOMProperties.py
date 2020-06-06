from typing import Dict, Union, Set

from ..base_schema import Schema


# TODO: DRY with object_schema.SchemaObject?

class DOMProperties(object):
    """
    A container for property information for a :class:`.DOMObject`.
    """

    properties: Dict[str, Schema] = None
    required: Set[str] = None
    additional_properties: Union[bool, Schema] = False

    def __init__(
            self,
            properties: Dict[str, Schema] = None,
            required: Set[str] = None,
            additional_properties: Union[bool, Schema] = False
    ) -> None:
        """
        :param properties:            A dictionary of :class:`~wysdom.base_schema.Schema` objects
                                      defining the expected names and types of a :class:`.DOMObject`'s
                                      properties.
        :param required:              A set of the property names that are required for an instance to be valid.
        :param additional_properties: Defines whether a :class:`.DOMObject` permits additional
                                      dynamically-named properties. Can be True or False, or
                                      can be set to a specific :class:`~wysdom.Schema` to restrict the permitted
                                      types of any additional properties.
        """
        self.properties = properties or {}
        self.required = required or set()
        self.additional_properties = additional_properties
