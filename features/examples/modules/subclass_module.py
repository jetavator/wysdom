from typing import Dict, List

from abc import ABC, abstractmethod

from wysdom import UserObject, UserProperty, SchemaArray, SchemaDict, SchemaConst
from wysdom.mixins import RegistersSubclasses


class Pet(RegistersSubclasses, UserObject, ABC):
    pet_type: str = UserProperty(str)
    name: str = UserProperty(str)

    @abstractmethod
    def speak(self):
        pass


class Dog(Pet):
    pet_type: str = UserProperty(SchemaConst("dog"))

    def speak(self):
        return f"{self.name} says Woof!"


class Cat(Pet):
    pet_type: str = UserProperty(SchemaConst("cat"))

    def speak(self):
        return f"{self.name} says Miaow!"


class Person(UserObject):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(str)
    pets: List[Pet] = UserProperty(SchemaArray(Pet))
