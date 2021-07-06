'''
Hooks that allow extension of the behaviour of steps, including output and validation
related steps. This also includes any hooks related to context expressions
'''
from typing import (
    Type,
    Dict,
    Tuple,
    Optional
)

from quilla.hookspecs import hookspec
from quilla.ctx import Context
from quilla.common.enums import UITestActions
from quilla.steps.base_steps import BaseStepFactory


StepFactorySelector = Dict[UITestActions, Type[BaseStepFactory]]


@hookspec
def quilla_step_factory_selector(selector: StepFactorySelector):
    '''
    A hook called immediately before resolving the step factory for a given step definition.
    This is used to register new step factories for custom step objects.

    Most custom steps should just add themselves to one of the non-factory selector hooks, but if
    a custom step requires complex logic it might be beneficial to register a factory to
    have more fine-grained control over the logic

    Args:
        selector: The factory selector dictionary.
    '''


@hookspec(firstresult=True)
def quilla_context_obj(ctx: Context, root: str, path: Tuple[str]) -> Optional[str]:
    '''
    A hook to allow pluggins to resolve a context object given its root
    and a path. All plugins that implement this hook *must* return None if they cannot
    resolve the context object.

    It is not possible to override the default context object handlers

    Args:
        ctx: The runtime context for the application
        root: The name of the context object, which is expressed as the root
            of a dot-separated path in the validation files
        path: The remainder of the context object path, where data is being
            retrieved from

    Returns
        the data stored at the context object if existing, None otherwise
    '''
