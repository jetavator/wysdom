.. toctree::
   :maxdepth: 2
   :caption: Contents:

User Documentation
##################


User objects API
=================

To build custom user object definitions in a declarative style,
you do so by creating subclasses of :class:`wysdom.UserObject`.
Instances of your subclass will behave as a `MutableMapping`,
so any code that works on the underlying dict that you use to
populate it should also work on the object instance.

There are two ways to add properties to a UserObject. The first
is to add named properties, by using the :class:`wysdom.UserProperty`
data descriptor::

    class Person(UserObject):
        first_name = UserProperty(str)

The second is to allow dynamically named additional properties::

    class Person(UserObject, additional_properties=True):
        ...

Any additional properties that are not explicitly defined as named
attributes using the UserProperty descriptor must be accessed
using the subscript style, `object_instance[property_name]`.

You may also restrict the data types of the additional properties
that you will allow. The type parameter that you pass in to
`additional_properties` can be a primitive Python type, a subclass
of :class:`~wysdom.UserProperty`, or an instance of :class:`~wysdom.Schema`::

    class Person(UserObject, additional_properties=str):
        ...

    class Person(UserObject, additional_properties=Address):
        ...

    class Person(UserObject, additional_properties=SchemaDict[Vehicle]):
        ...


Property Types
--------------

The type parameter that you pass in to :class:`~wysdom.UserProperty` can be a primitive
Python type, a subclass of :class:`~wysdom.UserProperty`, or an instance of :class:`~wysdom.Schema`::

    class Person(UserObject):
        first_name = UserProperty(str)
        last_name = UserProperty(str)
        current_address = UserProperty(Address)
        previous_addresses = UserProperty(SchemaArray(Address))
        vehicles = UserProperty(SchemaDict(Vehicle))

Property Naming
---------------

If a UserProperty is not explicitly given a name, it is populated using
the attribute name that it is given on the parent class. If you want
the name of the attribute in the class to be different from the
key in the underlying data that is supplied to the object, you
may specify it explicitly using the `name` parameter::

    class Person(UserObject):
        last_name = UserProperty(str, name="surname")

Defaults
--------

If you need a UserProperty to have a default value, you may give it
a static value using the `default` parameter::

    class Person(UserObject):
        first_name = UserProperty(str, default="")

Or if you need the default value to have a dynamic value based on other
properties, you may use the `default_function` parameter::

    class Person(UserObject):
        ...
        known_as = UserProperty(
            str,
            default_function=lambda person: person.first_name
        )

DOM functions
=============

While the DOM and schema information can be retrieved from a DOMElement
using the `__json_dom_info__` property and `__json_schema__()` method
respectively, the following convenience functions are provided
for code readability.

.. autofunction:: wysdom.document

.. autofunction:: wysdom.parent

.. autofunction:: wysdom.key

.. autofunction:: wysdom.schema


Mixins
======

The interface for UserObject has been kept as minimal as possible to
avoid cluttering the interfaces of user subclasses with unnecessary
methods. However, there is some common functionality, such as reading
and writing JSON and YAML

ReadsJSON
---------

Usage: As in the first usage example, but add :class:`wysdom.mixins.ReadsJSON`
to the bases of Person::

    class Person(UserObject, ReadsJSON):
        first_name = UserProperty(str)
        last_name = UserProperty(str)
        current_address = UserProperty(Address)
        previous_addresses = UserProperty(SchemaArray(Address))

    person_instance = Person.from_json(
        """
        {
          "first_name": "Marge",
          "last_name": "Simpson",
          "current_address": {
            "first_line": "123 Fake Street",
            "second_line": "",
            "city": "Springfield",
            "postal_code": 58008
          },
          "previous_addresses": [{
            "first_line": "742 Evergreen Terrace",
            "second_line": "",
            "city": "Springfield",
            "postal_code": 58008
          }],
          "vehicles": {
            "eabf04": {
              "color": "orange",
              "description": "Station Wagon"
            }
          }
        }
        """
    )


ReadsYAML
---------

Usage: As in the first usage example, but add :class:`wysdom.mixins.ReadsYAML`
to the bases of Person::

    class Person(UserObject, ReadsYAML):
        first_name = UserProperty(str)
        last_name = UserProperty(str)
        current_address = UserProperty(Address)
        previous_addresses = UserProperty(SchemaArray(Address))

    person_instance = Person.from_yaml(
        """
        first_name: Marge
        last_name: Simpson
        current_address:
          first_line: 123 Fake Street
          second_line: ''
          city: Springfield
          postal_code: 58008
        previous_addresses:
        - first_line: 742 Evergreen Terrace
          second_line: ''
          city: Springfield
          postal_code: 58008
        vehicles:
          eabf04:
            color: orange
            description: Station Wagon
        """
    )


RegistersSubclasses
-------------------

Use :class:`wysdom.mixins.RegistersSubclasses` as a mixin if you want an abstract base class to
have several more specific subclasses::

    class Pet(UserObject, RegistersSubclasses, ABC):
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


If you use RegistersSubclasses, you may refer to the abstract
base class when defining properties and schemas in wysdom. When
the DOM is populated with data, the subclass which matches the
supplied data's schema will automatically be chosen::

    class Person(UserObject):
        pets = UserProperty(SchemaArray(Pet))


    person_instance = Person({
        "pets": [{
            "pet_type": "dog",
            "name": "Santa's Little Helper"
        }]
    })

>>> type(person_instance.pets[0])
<class '__main__.Dog'>


If you include an abstract base class in an object definition, it will
be represented in the JSON schema using the `SchemaAnyOf` with all of
the defined subclasses as allowed options.


Registering classes by name
...........................

If your application needs to look up registered subclasses by a key,
you may supply the register_as keyword when declaring a subclass::

    class Elephant(Pet, register_as="elephant"):
        pet_type: str = UserProperty(SchemaConst("elephant"))

        def speak(self):
            return f"{self.name} says Trumpet!"

You may then use the class's registered name to look up the class or
create an instance from its parent class::

    >>> Pet.registered_subclass("elephant")
    <class '__main__.Elephant'>

    >>> Pet.registered_subclass_instance("elephant",
    ...     {"pet_type": "elephant", "name": "Stampy"}).speak()
    'Stampy says Trumpet!'


Internals
=========

Schemas
-------

Base schemas
............

The following schemas define simple atomic schemas
(defined in the subpackage `wysdom.base_schema`):

================================  ==================================================================
Name                              Description
================================  ==================================================================
:class:`~wysdom.Schema`           abstract base class
:class:`~wysdom.SchemaType`       abstract base class for any schema with the "type" directive
:class:`~wysdom.SchemaAnything`   any valid JSON will be accepted
:class:`~wysdom.SchemaConst`      a string constant
:class:`~wysdom.SchemaNone`       a null value
:class:`~wysdom.SchemaPrimitive`  a primitive variable
================================  ==================================================================

Object schemas
..............

The following schemas define complex schemas which reference other schemas
(defined in the subpackage `wysdom.object_schema`):

================================  ==================================================================
Name                              Description
================================  ==================================================================
:class:`~wysdom.SchemaAnyOf`      Any of the permitted schemas supplied
:class:`~wysdom.SchemaArray`      An array (corresponding to a Python list)
:class:`~wysdom.SchemaObject`     An object with named properties
:class:`~wysdom.SchemaDict`       An object with dynamic properties (corresponding to a Python dict)
================================  ==================================================================
