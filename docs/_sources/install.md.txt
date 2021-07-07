# Installation

## Recommended Python Version

Quilla was designed to work with Python 3.8+, and currently includes syntax that will cause errors in Python 3.7. Make sure you are using the correct version of python

## Installing Quilla with pip

> Note: A virtual environment is recommended. Python ships with `venv`, though other alternatives such as using `conda` or `virtualenvwrapper` are just as useful

Install Quilla by using `pip install quilla`.

The `pytest-quilla` plugin is also installed when installing quilla, though `pytest` is not. It is not necessary to install Pytest to run Quilla on its own. To download Pytest alongside Quilla, run `pip install quilla[pytest]` or `pip install pytest quilla` to install them separately.

## Installing Quilla from source

> Note: A virtual environment is recommended. Python ships with `venv`, though other alternatives such as using `conda` or `virtualenvwrapper` are just as useful

Download (or clone) the repository, and run `make install` to install Quilla. This will also expose the Quilla plugin to Pytest (if installed), though it will remain disabled until your pytest configuration file has the `use-quilla` option set to `True`. This does not cause any issues if Pytest is not installed, however, since it only registers the entrypoint.

## Installing Quilla from wheel files

It is occasionally necessary to install software in machines that either are not currently connected to the internet, or that cannot be connected to the internet. In these cases, it is still possible to install Quilla, although some setup will be required.

### Use pip to create the required wheel files

From a machine that can connect to PyPI, run `pip wheel quilla`, which will download all the `.whl` files from PyPI required to install Quilla. This will include all the dependencies listed in `setup.py`, but none of the extras. Move the `.whl` files to the target machine, and run `pip install ./*.whl` to install them.

### Package Quilla from source

> Packaging Quilla requires the `setuptools`, `pip`, and `wheel` packages. These should come default with every installation of Python, but if something seems to be going wrong make sure to check if they are installed.

Quilla comes bundled with a convenience Makefile that has multiple commands to make managing it simpler. For creating the `.whl` files from source, do the following:

1. Clone the repository
1. Run `make package-deps` to generate `.whl` files
    > Note: While this will generate a `.whl` from source for Quilla, it will still download the dependency `.whl` files from the package repository

1. Collect all files from the `dist/` folder (or whatever target folder you have decided) and move them to the target machine
1. Run `pip install ./*.whl`

## Customizing source install & build

The `Makefile` provided with Quilla uses several environment variables to configure its install and build process. All the available options are defined in the [makefile vars](makefile_vars.md) docs, including explanations on how they are used.
