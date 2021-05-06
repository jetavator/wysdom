from typing import List

from abc import ABC, abstractmethod

from wysdom import UserObject, UserProperty, SchemaArray, SchemaConst
from wysdom.mixins import RegistersSubclasses


class Pet(UserObject, RegistersSubclasses, ABC):
    pet_type: str = UserProperty(str)
    name: str = UserProperty(str)

    @abstractmethod
    def speak(self):
        pass


class Dog(Pet):
    def speak(self):
        return f"{self.name} says Woof!"


class Greyhound(Dog):
    pet_type: str = UserProperty(SchemaConst("greyhound"))

    def speak(self):
        return f"{self.name}, the greyhound, says Woof!"


class Person(UserObject):
    first_name: str = UserProperty(str)
    last_name: str = UserProperty(str)
    pets: List[Pet] = UserProperty(SchemaArray(Pet))


class Cat(Pet):
    pet_type: str = UserProperty(SchemaConst("cat"))

    def speak(self):
        return f"{self.name} says Miaow!"
