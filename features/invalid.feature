Feature: Test that invalid module specifications fail

  Scenario: Fail if both default and default_function are set

    When we try to load the Python module invalid_both_defaults.py
    Then a ValueError is raised with text:
      """
      Cannot use both default and default_function.
      """

  Scenario: Fail if both default is set and optional is set to False

    When we try to load the Python module invalid_required_and_default.py
    Then a ValueError is raised with text:
      """
      Cannot set optional to False if default or default_function are specified.
      """