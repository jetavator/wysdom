from typing import Dict, List

from wysdom import UserObject, UserProperty, SchemaArray, SchemaDict, key


class Vehicle(UserObject):
    color: str = UserProperty(str)
    description: str = UserProperty(str)

    @property
    def license(self):
        return key(self)


class Address(UserObject):
    first_line: str = UserProperty(str)
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
    vehicles: Dict[str, Vehicle] = UserProperty(SchemaDict(Vehicle), default={}, persist_defaults=True)
