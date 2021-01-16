Feature: Test subclassed DOM objects

  Scenario Outline: Test good input string

    Given the Python module <module>.py
    When we execute the following python code:
      """
      example_dict_input = {
        "first_name": "Marge",
        "last_name": "Simpson",
        "pets": [
          {
            "pet_type": "greyhound",
            "name": "Santa's Little Helper",
          },
          {
            "pet_type": "cat",
            "name": "Snowball II",
          }
        ]
      }
      example = <module>.Person(example_dict_input)
      expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$ref": "#/definitions/<module>.Person",
        "definitions": {
          "<module>.Greyhound": {
            "type": "object",
            "properties": {
              "pet_type": {"const": "greyhound"},
              "name": {"type": "string"}
            },
            "required": ["name", "pet_type"],
            "additionalProperties": False
          },
          "<module>.Cat": {
            "type": "object",
            "properties": {
              "pet_type": {"const": "cat"},
              "name": {"type": "string"}
            },
            "required": ["name", "pet_type"],
            "additionalProperties": False
          },
          "<module>.Pet": {
            "anyOf": [
              {"$ref": "#/definitions/<module>.Greyhound"},
              {"$ref": "#/definitions/<module>.Cat"}
            ]
          },
          "<module>.Person": {
            "type": "object",
            "properties": {
              "first_name": {"type": "string"},
              "last_name": {"type": "string"},
              "pets": {
                "array": {
                  "items": {"$ref": "#/definitions/<module>.Pet"}
                }
              }
            },
            "required": ["first_name", "last_name", "pets"],
            "additionalProperties": False
          }
        }
      }
      """
    Then the following statements are true:
      """
      example.first_name == "Marge"
      example.last_name == "Simpson"
      example.pets[0].pet_type == "greyhound"
      example.pets[0].name == "Santa's Little Helper"
      example.pets[0].speak() == "Santa's Little Helper, the greyhound, says Woof!"
      example.pets[1].pet_type == "cat"
      example.pets[1].name == "Snowball II"
      example.pets[1].speak() == "Snowball II says Miaow!"
      schema(example).is_valid(example_dict_input)
      schema(example).jsonschema_full_schema == expected_schema
      example.to_builtin() == example_dict_input
      copy.copy(example).to_builtin() == example_dict_input
      copy.deepcopy(example).to_builtin() == example_dict_input
      """

    Examples:
      | module               |
      | subclass_module      |
      | late_subclass_module |

