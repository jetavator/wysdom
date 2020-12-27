Feature: Generic mixin for registering subclasses by name

  Scenario: Test basic usage

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def __init__(self, name):
          self.name = name

        def speak(self):
          raise NotImplementedError()

      class Dog(Animal, register_as="dog"):

        def speak(self):
          return f"{self.name} says Woof!"

      class Cat(Animal, register_as="cat"):

        def speak(self):
          return f"{self.name} says Miaow!"
      """
    Then the following statements are true:
      """
      Animal.registered_subclass("dog") is Dog
      Animal.registered_subclass("cat") is Cat
      type(Animal.registered_subclass_instance("dog", "Spot")) is Dog
      type(Animal.registered_subclass_instance("cat", "Whiskers")) is Cat
      Animal.registered_subclass_instance("dog", "Spot").speak() == "Spot says Woof!"
      Animal.registered_subclass_instance("cat", "Whiskers").speak() == "Whiskers says Miaow!"
      """

  Scenario: Allow more distant descendants to be registered

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def speak(self):
          raise NotImplementedError()

      class Pet(Animal):

        def __init__(self, name):
          self.name = name

      class Dog(Pet, register_as="dog"):

        def speak(self):
          return f"{self.name} says Woof!"

      class Cat(Pet, register_as="cat"):

        def speak(self):
          return f"{self.name} says Miaow!"
      """
    Then the following statements are true:
      """
      Animal.registered_subclass("dog") is Dog
      Animal.registered_subclass("cat") is Cat
      Pet.registered_subclass("dog") is Dog
      Pet.registered_subclass("cat") is Cat
      type(Pet.registered_subclass_instance("dog", "Spot")) is Dog
      type(Pet.registered_subclass_instance("cat", "Whiskers")) is Cat
      Pet.registered_subclass_instance("dog", "Spot").speak() == "Spot says Woof!"
      Pet.registered_subclass_instance("cat", "Whiskers").speak() == "Whiskers says Miaow!"
      """

  Scenario: Raise KeyError when a class key is not defined

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def __init__(self, name):
          self.name = name
      """
    And we try to execute the following python code:
      """
      Animal.registered_subclass("elephant")
      """
    Then a KeyError is raised with text:
      """
      The key 'elephant' matches no proper subclasses of <class 'Animal'>.
      """

  Scenario: Raise KeyError when a class key is only defined on a superclass

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def speak(self):
          raise NotImplementedError()

      class Pet(Animal):

        def __init__(self, name):
          self.name = name

      class Dog(Pet, register_as="dog"):

        def speak(self):
          return f"{self.name} says Woof!"

      class Cat(Animal, register_as="cat"):

        def speak(self):
          return f"Cat says Miaow!"
      """
    And we try to execute the following python code:
      """
      Pet.registered_subclass("cat")
      """
    Then a KeyError is raised with text:
      """
      The key 'cat' matches no proper subclasses of <class 'Pet'>.
      """

  Scenario: Raise KeyError when a class key matches more than one subclass

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def __init__(self, name):
          self.name = name

        def speak(self):
          raise NotImplementedError()

      class Dog(Animal, register_as="animal"):

        def speak(self):
          return f"{self.name} says Woof!"

      class Cat(Animal, register_as="animal"):

        def speak(self):
          return f"{self.name} says Miaow!"
      """
    And we try to execute the following python code:
      """
      Animal.registered_subclass("animal")
      """
    Then a KeyError is raised with text:
      """
      The key 'animal' is ambiguous as it matches multiple proper subclasses of <class 'Animal'>:
      [<class 'Dog'>, <class 'Cat'>]
      """

  Scenario: Allow non-unique register_as values for different inheritance paths

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def speak(self):
          raise NotImplementedError()

      class Pet(Animal):

        def __init__(self, name):
          self.name = name

      class Dog(Animal, register_as="dog"):

        def speak(self):
          return f"The dog says Woof!"

      class PetDog(Pet, Dog, register_as="dog"):

        def speak(self):
          return f"{self.name} says Woof!"
      """

    Then the following statements are true:
      """
      Animal.registered_subclass("dog") is Dog
      Pet.registered_subclass("dog") is PetDog
      type(Animal.registered_subclass_instance("dog")) is Dog
      type(Pet.registered_subclass_instance("dog", "Spot")) is PetDog
      Animal.registered_subclass_instance("dog").speak() == "The dog says Woof!"
      Pet.registered_subclass_instance("dog", "Spot").speak() == "Spot says Woof!"
      """


  Scenario: Raise KeyError if return_common_superclass is False and class names are ambiguous

    When we execute the following python code:
      """
      from wysdom.mixins import RegistersSubclasses

      class Animal(RegistersSubclasses):

        def speak(self):
          raise NotImplementedError()

      class Pet(Animal):

        def __init__(self, name):
          self.name = name

      class Dog(Animal, register_as="dog"):

        def speak(self):
          return f"The dog says Woof!"

      class PetDog(Pet, Dog, register_as="dog"):

        def speak(self):
          return f"{self.name} says Woof!"
      """

    And we try to execute the following python code:
      """
      Animal.registered_subclass("dog", return_common_superclass=False)
      """
    Then a KeyError is raised with text:
      """
      The key 'dog' is ambiguous as it matches multiple proper subclasses of <class 'Animal'>:
      [<class 'Dog'>, <class 'PetDog'>]
      """