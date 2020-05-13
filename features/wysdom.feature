Feature: Test JSON DOM objects

  Scenario: Test good input string

    Given the Python module example.py
    And the following string, example_json
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
    When we evaluate the following python code in the variable example:
      """
      context.module.Example.from_json(context.example_json)
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

    Given the Python module example.py
    And the following string, example_json
      """
      {"foo": "bar"}
      """
    Then the following statement raises ValidationError
      """
      context.module.Example.from_json(context.example_json)
      """