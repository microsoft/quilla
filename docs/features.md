# Features

## Declarative JSON UI Testing

Write all your UI test cases in JSON using Quilla's declarative syntax. Focus on *what* your tests do, not *how* you do them!

Check out how to write your validation files [here](validation_files.md).

## Dynamic Validation Files with Context Expressions

Most UI validations have well-defined and easy to reproduce steps that can be defined statically. For all those that need a little extra, context expressions can give you just the edge you need. You'll never have to worry about writing passwords in your validation files with the bundled `Environment` context object, which lets you use environment variables in your UI validations.

Need to use values you produce yourself further on in your testing? With the `Validation` context object, you can consume your outputs seamlessly!

Check out all these and more in the context expressions documentation [here](context_expressions.md)

## Extensive Plugin System

Quilla has an extensive plugin system to allow users to customize their own experience, and to further extend the functionality that it can do! Check out how to write your first `uiconf.py` local plugin file, and how to release new plugins [here](plugins.md), and make sure to check out the documentation for `quilla.hookspecs` for the most up-to-date hooks and how to use them!

## JSON Reporting and Outputs

Interact with Quilla output programmatically, and act on the results of your Quilla tests easily! All Quilla results are returned as a JSON string which you can pass to other applications, display neatly with the `--pretty` flag, or publish as part of your CI/CD.

Did you produce values you will then need later on in your build pipeline? Collect it from the resulting JSON through the `"Outputs"` object!

## Pytest Integration

Quilla also functions as a `pytest` plugin! Just add `use-quilla: True` to your Pytest configuration, and you can immediately add all your quilla tests to your pre-existing testing suite!

Using the `pytest-quilla` plugin (which is installed alongside `quilla`) lets you take advantage of an already-existing and thriving community of testers! Add concurrency to your quilla tests through `pytest-xdist` with the assurance that each of your Quilla tests will be executed with an isolated context, enhance your testing output through one of many visual plugins, and benefit from the familiar `pytest` test discovery and reporting paradigm.

Check out the `pytest-quilla` documentation [here](quilla_pytest.md)!
