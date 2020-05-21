Feature: Test JSON DOM objects

  Scenario: Test good input string

    Given the Python module json_module.py
    And the following string, example_json_input
      """
      {
        "services": {
          "spark": {
            "type": "local_spark"
          }
        },
        "storage": {
          "vault": "spark",
          "star": "spark",
          "logs": "spark"
        },
        "compute": "spark"
      }
      """
    When we execute the following python code:
      """
      example = json_module.Example.from_json(example_json_input)
      example_json_output = example.to_json()
      """
    Then the following statements are true:
      """
      example.storage.vault == "spark"
      example.storage["vault"] == "spark"
      example.services["spark"].type == "local_spark"
      example["services"]["spark"]["type"] == "local_spark"
      len(example) == 3
      len(example.storage) == 3
      parent(example.services) is example
      document(example.services) is example
      key(example.services) == "services"
      parent(example.services["spark"]) is example.services
      document(example.services["spark"]) is example
      key(example.services["spark"]) == "spark"
      parent(example["services"]["spark"]) is example.services
      document(example["services"]["spark"]) is example
      key(example["services"]["spark"]) == "spark"
      json.JSONDecoder().decode(example_json_output) == json.JSONDecoder().decode(example_json_input)
      """

  Scenario: Test file loading

    Given the Python module json_module.py
    When we execute the following python code:
      """
      example = json_module.Example.from_json_file("./features/examples/data/example.json")
      example_json_output = example.to_json()
      """
    Then the following statements are true:
      """
      example.storage.vault == "spark"
      example.storage["vault"] == "spark"
      example.services["spark"].type == "local_spark"
      example["services"]["spark"]["type"] == "local_spark"
      len(example) == 3
      len(example.storage) == 3
      parent(example.services) is example
      document(example.services) is example
      key(example.services) == "services"
      parent(example.services["spark"]) is example.services
      document(example.services["spark"]) is example
      key(example.services["spark"]) == "spark"
      parent(example["services"]["spark"]) is example.services
      document(example["services"]["spark"]) is example
      key(example["services"]["spark"]) == "spark"
      """

  Scenario: Test bad input string

    Given the Python module json_module.py
    And the following string, example_json_input
      """
      {"foo": "bar"}
      """
    Then the following statement raises ValidationError
      """
      json_module.Example.from_json(example_json_input)
      """