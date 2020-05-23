from typing import Dict, List

from wysdom import UserObject, UserProperty, SchemaArray, SchemaDict, key


class Vehicle(UserObject, register_as="vehicle"):
    color: str = UserProperty(str)
    description: str = UserProperty(str)

    @property
    def license(self):
        return key(self)


class Address(UserObject, register_as="address"):
    first_line: str = UserProperty(str)
    second_line: str = UserProperty(str)
    city: str = UserProperty(str)
    postal_code: str = UserProperty(int)


class Person(UserObject, register_as="person"):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(str)
    current_address: Address = UserProperty(Address)
    previous_addresses: List[Address] = UserProperty(SchemaArray(Address))
    vehicles: Dict[str, Vehicle] = UserProperty(SchemaDict(Vehicle))
