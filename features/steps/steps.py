from behave import *

import wysdom
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
        context.exception = None
    except Exception as e:
        context.exception = e


@then("a {exception_type} is raised with text")
def step_impl(context, exception_type):
    if context.exception is None:
        raise Exception("No exception was raised.")
    if exception_type != context.exception.__class__.__name__:
        raise Exception(
            f"Expected exception type {exception_type}, got {type(context.exception)}: " +
            str(context.exception)
        )

    def remove_whitespace(text):
        return " ".join(
            line.strip('"')
            for line in text.splitlines()
        ).strip()

    if remove_whitespace(context.text) != remove_whitespace(str(context.exception)):
        raise Exception(
            f"""
            Expected error message:
            {remove_whitespace(context.text)}
            Got:
            {remove_whitespace(str(context.exception))}
            """
        )


@given(u"the following string, {variable_name}")
def step_impl(context, variable_name):
    globals()[variable_name] = context.text


@when("we execute the following python code")
def execute_python(context):
    exec(context.text)
    globals().update(locals())


@when("we try to execute the following python code")
def step_impl(context):
    context.scenario.text = context.text
    try:
        execute_python(context)
        context.exception = None
    except Exception as e:
        context.exception = e


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
