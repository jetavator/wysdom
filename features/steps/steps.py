from behave import *

from wysdom import document, parent, key, schema

import os
import importlib.util
import yaml
import json
import copy


@given("the Python module {module}.py")
def load_python_module(context, module):
    spec = importlib.util.spec_from_file_location(
        module,
        os.path.join(
            context.config.paths[0],
            f"examples/modules/{module}.py"
        )
    )
    loaded_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded_module)
    globals()[module] = loaded_module


@when("we try to load the Python module {module}.py")
def step_impl(context, module):
    try:
        load_python_module(context, module)
        context.load_python_module_error = None
    except Exception as e:
        context.load_python_module_error = e


@then("a {exception_type} is raised with text")
def step_impl(context, exception_type):
    if context.load_python_module_error is None:
        raise Exception("No exception was raised.")
    if exception_type != context.load_python_module_error.__class__.__name__:
        raise Exception(
            f"Expected exception type {exception_type}, got {type(context.load_python_module_error)}."
        )
    if context.text.strip() != str(context.load_python_module_error).strip():
        raise Exception(
            f"Expected error message '{context.text}', got '{context.load_python_module_error}'."
        )


@given(u"the following string, {variable_name}")
def step_impl(context, variable_name):
    globals()[variable_name] = context.text


@when("we execute the following python code")
def step_impl(context):
    exec(context.text)
    globals().update(locals())


@then("the following statements are true")
def step_impl(context):
    assert callable(document)
    assert callable(parent)
    assert callable(key)
    assert callable(schema)
    for line in context.text.splitlines():
        result = eval(line)
        if not result:
            raise Exception(f"{line} had result {result}")


@then("the following statement raises {exception_type}")
def step_impl(context, exception_type):
    try:
        eval(context.text)
        raise Exception("No error was raised as expected")
    except Exception as e:
        if e.__class__.__name__ != exception_type:
            raise


@then("the list {variable_name} contains the following tuples")
def step_impl(context, variable_name):
    tuple_list = eval(variable_name)

    def matches(a, b):
        return a is b or a == b

    for x in context.table:
        if not any(
            matches(y.element, eval(x["element"]))
            and matches(y.document, eval(x["document"]))
            and matches(y.parent, eval(x["parent"]))
            and matches(y.element_key,  eval(x["element_key"]))
            for y in tuple_list
        ):
            raise Exception(f"Could not find {x}")
    if len(list(context.table)) != len(tuple_list):
        raise Exception("Lengths of lists do not match")
