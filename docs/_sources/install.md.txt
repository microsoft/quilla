# Installation

## Recommended Python Version

Quilla was designed to work with Python 3.8+, and currently includes syntax that will cause errors in Python 3.7. Make sure you are using the correct version of python

## Installing Quilla

<!-- TODO: Update docs if it gets deployed to PyPI to reflect easy installation with `pip` -->

> Note: A virtual environment is recommended. Python ships with `venv`, though other alternatives such as using `conda` or `virtualenvwrapper` are just as useful

Download (or clone) the repository, and run `make install` to install Quilla. This will also expose the Quilla plugin to Pytest (if installed), though it will remain disabled until your pytest configuration file has the `use-quilla` option set to `True`. This does not cause any issues if Pytest is not installed, however, since it only registers the entrypoint.

## Packaging the Python Code

Packaging Quilla requires the `setuptools`, `pip`, and `wheel` packages. These should come default with every installation of Python, but if something seems to be going wrong make sure to check if they are installed.

The preferred method of packaging Quilla is by using the `make` commands that come bundled with the project. Use `make package` to create (by default) the source and wheel distributions of Quilla, and use `make package-deps` to create a Quilla `.whl` file and all the `.whl` files required by Quilla as dependencies.

## Customizing install & build

The `Makefile` provided with Quilla uses several environment variables to configure its install and build process. All the available options are defined in the [makefile vars](makefile_vars.md) docs, including explanations on how they are used.
