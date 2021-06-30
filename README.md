# Quilla

[![CodeQL Code Analysis](https://img.shields.io/github/workflow/status/microsoft/quilla/CodeQL?label=CodeQL&logo=Github)](https://github.com/microsoft/quilla/actions/workflows/codeql-analysis.yml)
[![Test pipeline](https://img.shields.io/github/workflow/status/microsoft/quilla/Test%20pipeline?label=Tests&logo=Github)](https://github.com/microsoft/quilla/actions/workflows/test-pipeline.yml)
[![Release pipeline](https://img.shields.io/github/workflow/status/microsoft/quilla/Release%20pipeline?label=Release&logo=Github)](https://github.com/microsoft/quilla/actions/workflows/release-pipeline.yml)
[![Documentation publish](https://img.shields.io/github/deployments/microsoft/quilla/github-pages?label=Documentation&logo=Github)](https://microsoft.github.io/quilla)

[![License](https://img.shields.io/pypi/l/quilla?logo=github&logoColor=white&label=License)](https://github.com/microsoft/quilla/blob/main/LICENSE)
[![Package Version](https://img.shields.io/pypi/v/quilla?logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/quilla/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/quilla?logo=pypi&logoColor=white&label=Python)](https://github.com/microsoft/quilla)
[![Pypi Downloads](https://img.shields.io/pypi/dm/quilla?logo=pypi&logoColor=white&label=Downloads)](https://pypi.org/project/quilla/)

<!-- THIS SECTION SHOULD BE COPY+PASTED INTO THE docs/intro.md FILE -->
## Declarative UI Testing with JSON

Quilla is a framework that allows test-writers to perform UI testing using declarative syntax through JSON files. This enables test writers, owners, and maintainers to focus not on how to use code libraries, but on what steps a user would have to take to perform the actions being tested. In turn, this allows for more agile test writing and easier-to-understand test cases.

Quilla was built to be run in CI/CD, in containers, and locally. It also comes with an optional integration with [pytest](https://pytest.org), so you can write your Quilla test cases as part of your regular testing environment for python-based projects. Check out the [quilla-pytest](docs/quilla_pytest.md) docs for more information on how to configure `pytest` to auto-discover Quilla files, adding markers, and more.

Check out the [features](docs/features.md) docs for an overview of all quilla can do!

## Quickstart

1. Run `pip install quilla`
1. Ensure that you have the correct browser and drivers. Quilla will autodetect drivers that are in your PATH or in the directory it is called
1. Write the following as `Validation.json`, substituting "Edge" for whatever browser you have installed and have the driver for:

    ```json
    {
      "targetBrowsers": ["Edge"],
      "path": "https://www.bing.com",
      "steps": [
        {
          "action": "Validate",
          "type": "URL",
          "state": "Contains",
          "target": "bing",
        }
      ]
    }
    ```

1. Run `quilla -f Validation.json`

## Installation

> Note: It is **highly recommended** that you use a virtual environment whenever you install new python packages.
You can install Quilla by cloning the repository and running `make install`.

Quilla is available on [PyPI](https://pypi.org/project/quilla/), and can be installed by running `pip install quilla`.

For more information on installation options (such as installing from source) and packaging Quilla for remote install, check out the documentation for it [here](docs/install.md)

## Usage

This module can be used both as a library, a runnable module, as well as as a command-line tool. The output of `quilla --help` is presented below:

```text
usage: quilla [-h] [-f] [--debug] [--driver-dir DRIVERS_PATH] [-P] [--no-sandbox] [-d file] json

Program to provide a report of UI validations given a json representation of the validations or given the filename
containing a json document describing the validations

positional arguments:
  json                  The json file name or raw json string

optional arguments:
  -h, --help            show this help message and exit
  -f, --file            Whether to treat the argument as raw json or as a file
  --debug               Enable debug mode
  --driver-dir DRIVERS_PATH
                        The directory where browser drivers are stored
  -P, --pretty          Set this flag to have the output be pretty-printed
  --no-sandbox          Adds '--no-sandbox' to the Chrome and Edge browsers. Useful for running in docker containers'
  -d file, --definitions file
                        A file with definitions for the 'Definitions' context object
```

## Writing Validation Files

Check out the documentation for it [here](docs/validation_files.md)

## Context Expressions

This package is able to dynamically inject different values, exposed through context objects and expressions whenever the validation JSON would ordinarily require a regular string (instead of an enum). This can be used to grab values specified either at the command-line, or through environment variables.

More discussion of context expressions and how to use them can be found in the documentation file [here](docs/context_expressions.md)

## Generating Documentation

Documentation can be generated through the `make` command `make docs`

Check out the documentation for it [here](docs/README.md)

## Make commands

A Makefile is provided with several convenience commands. You can find usage instructions with `make help`, or below:

```text
Usage:
  make [target]

Targets:
  help                            Print this help message and exit
  package                         Create release packages
  package-deps                    Create wheel files for all runtime dependencies
  docs                            Build all the docs in the docs/_build directory
  clean-python                    Cleans all the python cache & egg files files
  clean-docs                      Clean the docs build directory
  clean-build                     Cleans all code build and distribution directories
  clean                           Cleans all build, docs, and cache files
  install                         Installs the package
  install-docs                    Install the package and docs dependencies
  install-tests                   Install the package and test dependencies
  install-all                     Install the package, docs, and test dependencies
```

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
