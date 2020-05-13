from behave import *

from wysdom import document, parent, key, UserObject

import os
import importlib.util


@given("the Python module {module}.py")
def step_impl(context, module):
    spec = importlib.util.spec_from_file_location(
        module,
        os.path.join(
            context.config.paths[0],
            f"examples/modules/{module}.py"
        )
    )
    context.module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(context.module)


@step(u"the following string, {variable_name}")
def step_impl(context, variable_name):
    setattr(context, variable_name, context.text)


@when("we evaluate the following python code in the variable example")
def step_impl(context):
    context.example = eval(context.text)


@then("the following statements are true")
def step_impl(context):
    example = context.example
    assert callable(document)
    assert callable(parent)
    assert callable(key)
    assert isinstance(example, UserObject)
    for line in context.text.splitlines():
        result = eval(line)
        if not result:
            raise Exception(f"{line} had result {result}")


@when("we try run the following python code")
def step_impl(context):
    raise NotImplementedError


@then("the following statement raises {exception_type}")
def step_impl(context, exception_type):
    try:
        eval(context.text)
        raise Exception("No error was raised as expected")
    except Exception as e:
        if e.__class__.__name__ != exception_type:
            raise
