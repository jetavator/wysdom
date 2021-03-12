Feature: Test dictionary DOM objects

  Scenario: Test good input string

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
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
      example = dict_module.Person(example_dict_input)
      example_dict_output = example.to_builtin()
      expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$ref": "#/definitions/dict_module.Person",
        "definitions": {
          "dict_module.Address": {
            "type": "object",
            "properties": {
              "city": {"type": "string"},
              "first_line": {"type": "string", "pattern": r"^(\d)+.*$"},
              "second_line": {"type": "string"},
              "postal_code": {"type": "integer"}
            },
            "required": ["city", "first_line", "postal_code"],
            "additionalProperties": False
          },
          "dict_module.Vehicle": {
            "type": "object",
            "properties": {
              "color": {"enum": ["pink", "orange"]},
              "description": {"type": "string"}
            },
            "required": ["color", "description"],
            "additionalProperties": False
          },
          "dict_module.Person": {
            "type": "object",
            "properties": {
              "first_name": {"type": "string"},
              "last_name": {"type": "string"},
              "current_address": {"$ref": "#/definitions/dict_module.Address"},
              "previous_addresses": {
                "array": {
                  "items": {"$ref": "#/definitions/dict_module.Address"}
                }
              },
              "vehicles": {
                "properties": {},
                "required": [],
                "additionalProperties": {"$ref": "#/definitions/dict_module.Vehicle"},
                "propertyNames": {
                  "type": "string",
                  "pattern": r"^[a-f0-9]{6}$"
                },
                "type": "object"
              }
            },
            "required": ["first_name", "last_name", "previous_addresses"],
            "additionalProperties": False
          }
        }
      }
      walk_elements = list(example.walk_elements())
      """
    Then the following statements are true:
      """
      example.first_name == "Marge"
      example.last_name == "Simpson"
      example.current_address.first_line == "123 Fake Street"
      example.current_address.second_line == ""
      example.current_address.city == "Springfield"
      example.current_address.postal_code == 58008
      example["current_address"].first_line == "123 Fake Street"
      example["current_address"].second_line == ""
      example["current_address"].city == "Springfield"
      example["current_address"].postal_code == 58008
      example.previous_addresses[0].first_line == "742 Evergreen Terrace"
      example.previous_addresses[0].second_line == ""
      example.previous_addresses[0].city == "Springfield"
      example.previous_addresses[0].postal_code == 58008
      isinstance(example.vehicles["eabf04"].color, dict_module.Color)
      example.vehicles["eabf04"].color is dict_module.Color.ORANGE
      example.vehicles["eabf04"].description == "Station Wagon"
      example.vehicles["eabf04"].license == "eabf04"
      len(example) == 5
      len(example.current_address) == 4
      len(example.previous_addresses) == 1
      len(example.vehicles) == 1
      parent(example.current_address) is example
      document(example.current_address) is example
      key(example.current_address) == "current_address"
      parent(example.vehicles["eabf04"]) is example.vehicles
      document(example.vehicles["eabf04"]) is example
      key(example.vehicles["eabf04"]) == "eabf04"
      parent(example["vehicles"]["eabf04"]) is example.vehicles
      document(example["vehicles"]["eabf04"]) is example
      key(example["vehicles"]["eabf04"]) == "eabf04"
      schema(dict_module.Person).is_valid(example_dict_input)
      schema(dict_module.Person).jsonschema_full_schema == expected_schema
      example_dict_output == example_dict_input
      copy.copy(example).to_builtin() == example_dict_input
      copy.deepcopy(example).to_builtin() == example_dict_input
      set(properties(example).keys()) == {"first_name", "last_name", "current_address", "previous_addresses", "vehicles"}
      """
    And the list walk_elements contains the following tuples:
      | element                       | document | parent                        | element_key          |
      | example                       | example  | None                          | None                 |
      | "Marge"                       | example  | example                       | "first_name"         |
      | "Simpson"                     | example  | example                       | "last_name"          |
      | example.current_address       | example  | example                       | "current_address"    |
      | "123 Fake Street"             | example  | example.current_address       | "first_line"         |
      | ""                            | example  | example.current_address       | "second_line"        |
      | "Springfield"                 | example  | example.current_address       | "city"               |
      | 58008                         | example  | example.current_address       | "postal_code"        |
      | example.previous_addresses    | example  | example                       | "previous_addresses" |
      | example.previous_addresses[0] | example  | example.previous_addresses    | None                 |
      | "742 Evergreen Terrace"       | example  | example.previous_addresses[0] | "first_line"         |
      | ""                            | example  | example.previous_addresses[0] | "second_line"        |
      | "Springfield"                 | example  | example.previous_addresses[0] | "city"               |
      | 58008                         | example  | example.previous_addresses[0] | "postal_code"        |
      | example.vehicles              | example  | example                       | "vehicles"           |
      | example.vehicles["eabf04"]    | example  | example.vehicles              | "eabf04"             |
      | dict_module.Color.ORANGE      | example  | example.vehicles["eabf04"]    | "color"              |
      | "Station Wagon"               | example  | example.vehicles["eabf04"]    | "description"        |

  Scenario: Succeed if missing parameters are optional

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
        "first_name": "Marge",
        "last_name": "Simpson",
        "previous_addresses": [{
          "first_line": "742 Evergreen Terrace",
          "city": "Springfield",
          "postal_code": 58008
        }]
      }
      example = dict_module.Person(example_dict_input)
      """
    Then the following statements are true:
      """
      schema(dict_module.Person).is_valid(example_dict_input)
      example.current_address.second_line is None
      example.previous_addresses[0].second_line is None
      example.current_address.first_line == "742 Evergreen Terrace"
      len(example.vehicles) == 0
      """

  Scenario: Fail if missing parameters are non-optional

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
        "first_name": "Marge",
        "previous_addresses": [{
          "first_line": "742 Evergreen Terrace",
          "city": "Springfield",
          "postal_code": 58008
        }]
      }
      """
    Then the following statements are true:
      """
      not(schema(dict_module.Person).is_valid(example_dict_input))
      """
    And the following statement raises ValidationError
      """
      dict_module.Person(example_dict_input)
      """

  Scenario: Test bad input string

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {"foo": "bar"}
      """
    Then the following statements are true:
      """
      not(schema(dict_module.Person).is_valid(example_dict_input))
      """
    And the following statement raises ValidationError
      """
      dict_module.Person(example_dict_input)
      """

  Scenario: Defaults should not be written as permanent values when accessed

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
        "first_name": "Marge",
        "last_name": "Simpson",
        "previous_addresses": [{
          "first_line": "742 Evergreen Terrace",
          "city": "Springfield",
          "postal_code": 58008
        }]
      }
      example = dict_module.Person(example_dict_input)
      original_address = example.current_address
      example.previous_addresses[0] = {
        "first_line": "123 Fake Street",
        "city": "Springfield",
        "postal_code": 58008
      }
      """
    Then the following statements are true:
      """
      example.current_address.first_line == "123 Fake Street"
      example.previous_addresses[0].first_line == "123 Fake Street"
      type(example.vehicles) is wysdom.dom.DOMDict
      document(example.vehicles) is example
      example.vehicles is example.vehicles
      """

  Scenario: Test invalid value for property pattern

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
          "first_line": "Bad Address",
          "city": "Springfield",
          "postal_code": 58008
      }
      """
    Then the following statements are true:
      """
      not(schema(dict_module.Address).is_valid(example_dict_input))
      """
    And the following statement raises ValidationError
      """
      dict_module.Address(example_dict_input)
      """

  Scenario: Test invalid value for dictionary key pattern

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {
        "first_name": "Marge",
        "last_name": "Simpson",
        "current_address": {
          "first_line": "123 Fake Street",
          "second_line": "",
          "city": "Springfield",
          "postal_code": 58008
        },
        "previous_addresses": [],
        "vehicles": {
          "badkey": {
            "color": "orange",
            "description": "Station Wagon"
          }
        }
      }
      """
    Then the following statements are true:
      """
      not(schema(dict_module.Person).is_valid(example_dict_input))
      """
    And the following statement raises ValidationError
      """
      dict_module.Person(example_dict_input)
      """


  Scenario: Fail if pattern is supplied and property_type is not str

    When we try to load the Python module invalid_pattern_not_str.py
    Then a TypeError is raised with text:
      """
      Parameter 'pattern' can only be set if 'property_type' is str.
      """
