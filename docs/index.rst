.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. include:: ../README.rst


User objects API
=================

To build custom user object definitions in a declarative style,
you do so by creating subclasses of `wysdom.UserObject`.
Instances of your subclass will behave as a `MutableMapping`,
so any code that works on the underlying dict that you use to
populate it should also work on the object instance.

.. autoclass:: wysdom.UserObject
   :members:
   :inherited-members:

There are two ways to add properties to a UserObject. The first
is to add named properties, by using the `wysdom.UserProperty`
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
of `UserObject`, or an instance of `wysdom.Schema`::

    class Person(UserObject, additional_properties=str):
        ...

    class Person(UserObject, additional_properties=Address):
        ...

    class Person(UserObject, additional_properties=SchemaDict[Vehicle]):
        ...

.. autoclass:: wysdom.UserProperty
   :members:

Property Types
--------------

The type parameter that you pass in to `UserProperty` can be a primitive
Python type, a subclass of `UserObject`, or an instance of `wysdom.Schema`::

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

Usage: As in the first usage example, but add ReadsJSON to the
bases of Person::

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

.. autoclass:: wysdom.ReadsJSON
   :members:

ReadsYAML
---------

Usage: As in the first usage example, but add ReadsYAML to the
bases of Person::

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

.. autoclass:: wysdom.ReadsYAML
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
