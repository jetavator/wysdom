Feature: Test JSON DOM objects

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
      example_dict_output == example_dict_input
      """

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