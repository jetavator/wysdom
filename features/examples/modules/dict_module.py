from typing import Dict, List
from enum import Enum

from wysdom import UserObject, UserProperty, SchemaArray, SchemaDict, key


class Color(Enum):
    PINK = "pink"
    ORANGE = "orange"


class Vehicle(UserObject):
    color: Color = UserProperty(Color)
    description: str = UserProperty(str)

    @property
    def license(self):
        return key(self)


class Address(UserObject):
    first_line: str = UserProperty(str, pattern=r"^(\d)+.*$")
    second_line: str = UserProperty(str, optional=True)
    city: str = UserProperty(str)
    postal_code: str = UserProperty(int)


class Person(UserObject):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(str)
    current_address: Address = UserProperty(
        Address,
        default_function=lambda person: person.previous_addresses[0])
    previous_addresses: List[Address] = UserProperty(SchemaArray(Address))
    vehicles: Dict[str, Vehicle] = UserProperty(
        SchemaDict(Vehicle, key_pattern=r"^[a-f0-9]{6}$"),
        default={},
        persist_defaults=True)
