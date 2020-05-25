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
              "first_line": {"type": "string"},
              "postal_code": {"type": "integer"},
              "second_line": {"type": "string"}
            },
            "additionalProperties": False
          },
          "dict_module.Vehicle": {
            "type": "object",
            "properties": {
              "color": {"type": "string"},
              "description": {"type": "string"}
            },
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
                "additionalProperties": {"$ref": "#/definitions/dict_module.Vehicle"},
                "type": "object"
              }
            },
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
      example.vehicles["eabf04"].color == "orange"
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
      schema(example).is_valid(example_dict_input)
      schema(example).jsonschema_full_schema == expected_schema
      example_dict_output == example_dict_input
      copy.copy(example).to_builtin() == example_dict_input
      copy.deepcopy(example).to_builtin() == example_dict_input
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
      | "orange"                      | example  | example.vehicles["eabf04"]    | "color"              |
      | "Station Wagon"               | example  | example.vehicles["eabf04"]    | "description"        |

  Scenario: Test bad input string

    Given the Python module dict_module.py
    When we execute the following python code:
      """
      example_dict_input = {"foo": "bar"}
      """
    Then the following statements are true:
      """
      not(schema(example).is_valid(example_dict_input))
      """
    And the following statement raises ValidationError
      """
      dict_module.Person(example_dict_input)
      """