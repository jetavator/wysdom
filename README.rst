wysdom
######

|Python application| |docs| |codecov|

.. |Python application| image:: https://github.com/jetavator/wysdom/workflows/Python%20application/badge.svg
   :target: https://github.com/jetavator/wysdom

.. |docs| image:: https://readthedocs.org/projects/wysdom/badge/?version=latest
   :target: https://wysdom.readthedocs.io/en/latest/

.. |codecov| image:: https://codecov.io/gh/jetavator/wysdom/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jetavator/wysdom

A Python library for building custom document object models (DOMs) with built-in JSON schema
checking.


Motivation
----------

A common requirement in Python projects is to be able to load serialized structured data
into Python objects. Typically, you might begin by using dictionaries to store this data
and a library like json or PyYAML to parse the input.

However, this simple approach may create additional work elsewhere in your project, for
the following four reasons.

First, the serialized data you are loading might be user-generated, untrusted strings,
and so some validation is necessary to check that the document schema matches what you are
expecting.

Second, you may want to provide some promises to the rest of your application about the
attributes that exist in your data object and what their data types are. For example, given
a data object `config` which holds your application's configuration parameters, it is
preferable to know that `config.allow_nulls` is a `bool`, as opposed to the subscript
access style `config['allow_nulls']` which may return a KeyError or an unexpected data type.
This also enables your data objects to be covered by static type checking.

Third, you may want to add some additional functionality to your data objects in the form
of properties and methods, including within the substructure of your data object. For example,
a method `config.database.test_connection()`.

Fourth, you may want to pass some sub-elements of your data object to components in your
application, but have that sub-element retain awareness of the whole document. For example,
a class instance `db_service = DatabaseService(config.database)` might need to access some
attributes from the parent object `config`.


What wysdom does
----------------

With wysdom, you have one simple declarative way of defining the class structure of your
data objects. You can then instantiate a data object using raw data in dict form, or directly
deserialize it using one of wysdom's mixin classes.

Objects created by wysdom retain an awareness of the overall Document Object Model (DOM),
which can be queried using the supplied functions `document(obj)`, `parent(obj)` and
`key(obj)`.

Classes created by wysdom also auto-generate a JSON object schema and use the `jsonschema`
library to enable you to validate potential input.


Example Usage
-------------

User class definition::

    from wysdom import UserObject, UserProperty, SchemaArray

    class Address(UserObject):
        first_line = UserProperty(str)
        second_line = UserProperty(str)
        city = UserProperty(str)
        postal_code = UserProperty(int)

    class Person(UserObject):
        first_name = UserProperty(str)
        last_name = UserProperty(str)
        current_address = UserProperty(Address)
        previous_addresses = UserProperty(SchemaArray(Address))

Loading from dict::

    person_instance = Person({
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
      }]
    })

Reading attributes::

    >>> person_instance.last_name
    'Simpson'

    >>> person_instance.current_address.first_line
    '123 Fake Street'

    >>> person_instance.previous_addresses[0].first_line
    '742 Evergreen Terrace'
