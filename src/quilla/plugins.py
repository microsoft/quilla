from logging import Logger
import pkg_resources
from importlib.machinery import SourceFileLoader
from pathlib import Path

import pluggy

from quilla import hookspecs


_hookimpl = pluggy.HookimplMarker('quilla')


class _DummyHooks:
    '''
    A class of dummy hook implementations that do nothing
    '''

    @_hookimpl
    def quilla_addopts():  # type: ignore
        pass

    @_hookimpl
    def quilla_context_obj():  # type: ignore
        pass

    @_hookimpl
    def quilla_configure():  # type: ignore
        pass

    @_hookimpl
    def quilla_prevalidate():  # type: ignore
        pass

    @_hookimpl
    def quilla_postvalidate():  # type: ignore
        pass

    @_hookimpl
    def quilla_step_factory_selector():  # type: ignore
        pass

    @_hookimpl
    def quilla_configure_logger():  # type: ignore
        pass


def _get_uiconf_plugins(pm: pluggy.PluginManager, root: Path, logger: Logger):
    '''
    Attempts to load a conftest.py file on the root directory, and add all defined plugin
    hooks on that file into the plugin manager

    Args:
        pm: The plugin manager
        root: The directory in which to search for the conftest file
    '''

    uiconf_file = root / 'uiconf.py'
    if not uiconf_file.exists() or not uiconf_file.is_file():
        logger.info('Could not find uiconf file in %s', uiconf_file)
        return  # No plugin file to load

    abs_path = uiconf_file.expanduser().resolve()

    uiconf_module = SourceFileLoader('uiconf', str(abs_path)).load_module()

    logger.debug('Loading hooks from "uiconf" module')
    _load_hooks_from_module(pm, uiconf_module, logger)


def _load_hooks_from_module(pm: pluggy.PluginManager, module, logger: Logger):
    '''
    Load a module into the given plugin manager object by finding all
    methods in the module that start with the `quilla_` prefix
    and wrapping the in a _hookimpl so they are picked up by `pluggy`

    Args:
        pm: The plugin manager
        module: The loaded module instance
    '''
    hooks = filter(lambda x: x.find('quilla_') == 0, dir(hookspecs))

    for hook in hooks:
        if hasattr(module, hook):
            logger.debug('Found "%s" hook in module', hook)
            hook_function = getattr(module, hook)
            hook_function = _hookimpl(hook_function)
            setattr(module, hook, hook_function)

    logger.debug('Loading all discovered hooks into the plugin manager')
    pm.register(module)


def _load_entrypoint_plugins(pm: pluggy.PluginManager, logger: Logger):
    for entry_point in pkg_resources.iter_entry_points('QuillaPlugins'):
        logger.info('Found plugin module "%s" in entrypoints', entry_point.name)
        try:
            entry_point.require()
            _load_hooks_from_module(pm, entry_point.load(), logger)
        except pkg_resources.DistributionNotFound as e:
            # Skips package if it cannot load it
            logger.info(
                'Could not find proper distributions for %s plugin module',
                entry_point.name
            )
            logger.debug('Module encountered %s', e, exc_info=True)
            pass


def get_plugin_manager(path: str, logger: Logger) -> pluggy.PluginManager:
    '''
    Creates and configures a plugin manager by loading all the plugins defined
    through entrypoints or through a `uiconf.py` file found at the `path` location

    Args:
        path: the directory in which the `uiconf.py` will be found

    Returns:
        a configured PluginManager instance with all plugins already loaded
    '''
    pm = pluggy.PluginManager('quilla')
    logger.debug('Loading dummy hooks into plugin manager')
    pm.register(_DummyHooks)

    logger.debug('Loading entrypoint plugins')
    _load_entrypoint_plugins(pm, logger)

    logger.debug('Loading local "uiconf" plugin')
    _get_uiconf_plugins(pm, Path(path), logger)

    return pm
