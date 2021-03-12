from typing import Dict

from ..base_schema import Schema
from .UserObject import UserObject


def properties(user_object: UserObject) -> Dict[str, Schema]:
    """
    Retrieve the property names and their associated :class:`~wysdom.base_schema.Schema`
    objects for a particular `:class:`~wysdom.user_objects.UserObject.

    :param user_object: A `:class:`~wysdom.user_objects.UserObject
    :return:            A dictionary mapping property names to their :class:`~wysdom.base_schema.Schema`
    """
    return user_object.__json_schema_properties__.properties
