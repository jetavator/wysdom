Feature: Test YAML DOM objects

  Scenario: Test good input string

    Given the Python module yaml_module.py
    And the following string, example_yaml_input
      """
      services:
        spark:
          type: local_spark
      storage:
        vault: spark
        star: spark
        logs: spark
      compute: spark
      """
    When we execute the following python code:
      """
      example = yaml_module.Example.from_yaml(example_yaml_input)
      example_yaml_output = example.to_yaml()
      """
    Then the following statements are true:
      """
      isinstance(example, UserObject)
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
      yaml.safe_load(example_yaml_output) == yaml.safe_load(example_yaml_input)
      """

  Scenario: Test file loading

    Given the Python module yaml_module.py
    When we execute the following python code:
      """
      example = yaml_module.Example.from_yaml_file("./features/examples/data/example.yaml")
      example_yaml_output = example.to_yaml()
      """
    Then the following statements are true:
      """
      isinstance(example, UserObject)
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

    Given the Python module yaml_module.py
    And the following string, example_yaml_input
      """
      foo: bar
      """
    Then the following statement raises ValidationError
      """
      yaml_module.Example.from_yaml(example_yaml_input)
      """