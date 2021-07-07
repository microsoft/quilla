'''
Hooks that are related to configuration, such as logger configs, parser additions,
etc.
'''
from enum import Enum
from logging import Logger
from argparse import (
    ArgumentParser,
    Namespace
)
from typing import (
    Type,
    TypeVar,
    Optional,
)

from quilla.hookspecs import hookspec
from quilla.ctx import Context
from quilla.ui_validation import QuillaTest


T = TypeVar('T', bound=Enum)


@hookspec
def quilla_configure_logger(logger: Logger):
    '''
    A hook called immediately after the plugin manager is created. This is the very
    first hook called, and allows plugins to register additional handlers, formatters,
    or otherwise modify the logger used throughout Quilla. Note, the Context is not
    yet created

    To help in debugging, it is recommended that plugins register their own StreamHandler
    to the logger with a filter that shows only the messages relevant to the plugin.

    Args:
        logger: The configured logger instance for Quilla
    '''


@hookspec
def quilla_addopts(parser: ArgumentParser):
    '''
    A hook to allow plugins to add additional arguments to the argument parser.
    This can be used if a plugin requires additional parameters or data in some way.

    This is called after the initial argument parser setup

    Args:
        parser: The argparse Argument Parser instance used by the application
    '''


@hookspec
def quilla_configure(ctx: Context, args: Namespace):
    '''
    A hook to allow plugins to modify the context object, either changing its data
    or adding data to it.

    This is called after the initial setup of the context object

    Args:
        ctx: The runtime context for the application
        args: Parsed CLI args, in case they are needed
    '''


@hookspec
def quilla_prevalidate(validation: QuillaTest):
    '''
    A hook called immediately before the validations attempt to be resolved
    (i.e. before `validations.validate_all()` is called)

    Args:
        validation: The collected validations from the json passed to
            the application
    '''


@hookspec(firstresult=True)
def quilla_resolve_enum_from_name(name: str, enum: Type[T]) -> Optional[T]:
    '''
    A hook called when a value specified by the quilla test should be resolved to an
    enum, but no enum has been found. This is to allow plugins to register custom
    enum values for quilla, such as new step actions, validation types, validation states,
    output sources, etc.

    Args:
        name: the string value specified in the quilla test
        enum: The enum subclass type that is being attempted to be resolved. This
            should give an indication as to what is being resolved. For example,
            UITestActions is the enum type being resolved for the 'actions' field.

    Returns:
        The resolved enum, if it can be resolved. None if the plugin can't resolve
        the value.
    '''
