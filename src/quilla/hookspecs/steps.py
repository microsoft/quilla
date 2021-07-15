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

from quilla.hookspecs._hookspec import hookspec
from quilla.ctx import Context
from quilla.common.enums import (
    UITestActions,
    VisualParityImageType,
)
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


@hookspec(firstresult=True)
def quilla_store_image(
    ctx: Context,
    baseline_id: str,
    image_bytes: bytes,
    image_type: VisualParityImageType,
) -> Optional[str]:
    '''
    A hook to allow pluggins to store images for the VisualParity validation.

    Plugins should first check if they are able to authenticate or configure
    with whatever storage mechanism is being used to keep the baseline images,
    and return None if they cannot both read and write files. It is assumed that
    only one storage mechanism will be used for baseline/treatment images.

    If a plugin can write files to its storage mechanism, it should return the URI
    (i.e. the link, path, etc. that can be used to find the new image) so that it
    can be included in the report.

    Plugins to add storage mechanisms to VisualParity validations should implement
    this hook as well as the ``quilla_get_visualparity_baseline`` hook and some
    configuration method (i.e. adding CLI options with ``quilla_addopts`` or
    pulling data from the environment)

    Args:
        ctx: The runtime context for the application
        baseline_id: The image baseline ID associated with the image
        image_bytes: The data for the image PNG in bytes form
        image_type: The kind of image that it is, since different image types
            might be desired to be stored differently

    Returns
        An identifier that can locate the new image
    '''


@hookspec(firstresult=True)
def quilla_get_baseline_uri(ctx: Context, run_id: str, baseline_id: str) -> Optional[str]:
    '''
    A hook to allow plugins to retrieve some URI for the image associated with
    the baseline ID.

    Args:
        ctx: The runtime context of the application
        run_id: The run ID for the current run, in case the plugin tracks
            baselines for each run
        baseline_id: The unique ID for the baseline image

    Returns:
        An identifier that can locate the baseline image
    '''


@hookspec(firstresult=True)
def quilla_get_visualparity_baseline(ctx: Context, baseline_id: str) -> Optional[bytes]:
    '''
    A hook to allow pluggins to find baseline images for the VisualParity
    validation, called while the VisualParity validation step is being executed.

    Plugins should first check if they are able to authenticate or configure
    with whatever storage mechanism is being used to keep the baseline images,
    and return None if they cannot both read and write files. It is assumed that
    only one storage mechanism will be used for baseline/treatment images.

    If a plugin can read the files from its storage mechanism, it should search for the
    image by its baseline ID and return the data in bytes.

    Args:
        ctx: The runtime context for the application
        baseline_id: The baseline ID to search for

    Returns:
        The image data in bytes
    '''
