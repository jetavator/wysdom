wysdom
######

|Python application| |codecov|

.. |Python application| image:: https://github.com/jetavator/wysdom/workflows/Python%20application/badge.svg
   :target: https://github.com/jetavator/wysdom

.. |codecov| image:: https://codecov.io/gh/jetavator/wysdom/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jetavator/wysdom

A Python library for building custom document object models (DOMs) with built-in JSON schema checking

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
