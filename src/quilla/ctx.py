import os
import re
from functools import lru_cache
from typing import (
    Optional,
    List,
    Dict,
    cast
)
from pathlib import Path
from logging import (
    Logger,
    getLogger,
    NullHandler,
)
import json

from pluggy import PluginManager
import pydeepmerge as pdm

from quilla.common.exceptions import (
    InvalidContextExpressionException,
    InvalidOutputName,
)
from quilla.common.utils import DriverHolder


class Context(DriverHolder):
    '''
    Class defining configurations for the runtime context. This object
    should not be created directly but retrieved with "get_default_context"

    Args:
        plugin_manager: A configured PluginManager instance
        debug: Whether the configurations should be run as debug mode.
        drivers_path: The directory where the different browser drivers are stored
        pretty: If the output should be pretty-printed
        json_data: The json describing the validations
        is_file: Whether a file was originally passed in or if the raw json was passed in
        no_sandbox: Whether to pass the '--no-sandbox' arg to Chrome and Edge
        logger: An optional configured logger instance.


    Attributes:
        pm: A PluginManager instance with all hooks already loaded
        suppress_exceptions: Whether to suppress exceptions by generating reports or
            to crash the application on exception
        run_headless: Whether the browsers should be instructed to run headless
        close_browser: Whether the cleanup process should close browsers or leave the
            session open
        pretty: If the output should be pretty-printed
        json_data: The json describing the validations
        is_file: Whether a file was originally passed in or if raw json was passed in
        no_sandbox: Whether to pass the '--no-sandbox' arg to Chrome and Edge
        logger: A logger instance. If None was passed in for the 'logger' argument, will create
            one with the default logger.
    '''
    default_context: Optional["Context"] = None
    _drivers_path: str
    _expression_regex = re.compile(r'\${{(.*)}}')
    _context_obj_expression = re.compile(
        # Used on the inside of the _expession_regex to
        # find context objects embedded into the
        # context expression regex
        r'([a-zA-Z][a-zA-Z0-9_]+)(\.[a-zA-Z_][a-zA-Z0-9_]+)+'
    )
    _output_browser: str = 'Firefox'
    pretty_print_indent: int = 4

    def __init__(
        self,
        plugin_manager: PluginManager,
        debug: bool = False,
        drivers_path: str = '.',
        pretty: bool = False,
        json_data: str = '',
        is_file: bool = False,
        no_sandbox: bool = False,
        definitions: List[str] = [],
        logger: Optional[Logger] = None
    ):
        super().__init__()
        self.pm = plugin_manager
        self._path = os.environ['PATH']  # snapshot the path
        self.is_debug = debug
        self.pretty = pretty
        self.json = json_data
        self.is_file = is_file
        self.no_sandbox = no_sandbox
        path = Path(drivers_path)

        if logger is None:
            self.logger = getLogger('quilla')
            self.logger.addHandler(NullHandler())
        else:
            self.logger = logger

        self.drivers_path = str(path.resolve())
        self._context_data: Dict[str, dict] = {'Validation': {}, 'Outputs': {}, 'Definitions': {}}
        self._load_definition_files(definitions)

    @property
    def is_debug(self) -> bool:
        '''
        A set of debug configurations. Will return true if 'debug' is originally passed or
        this property is set, but one could edit the individual permissions to make a more
        fine-tuned debugging experience
        '''

        return self._debug

    @is_debug.setter
    def is_debug(self, v: bool):
        self._debug = v
        self.suppress_exceptions: bool = not v
        self.run_headless: bool = not v
        self.close_browser: bool = not v

    @property
    def drivers_path(self) -> str:
        '''
        The path where the drivers will be stored. Setting this property will add it to
        the PATH variable, so if the drivers are already in the PATH this can be omitted.
        '''
        return self._drivers_path

    @drivers_path.setter
    def drivers_path(self, v: str) -> str:
        path = Path(v)
        driver_path_str = str(path.resolve())
        self.logger.debug('Setting driver path to "%s"', driver_path_str)
        self._drivers_path = driver_path_str
        self._set_path()

        return v

    def _set_path(self):
        os.environ['PATH'] = f"{self._path}:{self._drivers_path}"

    @lru_cache
    def perform_replacements(self, text: str) -> str:
        '''
        Extracts any relevant context expressions from the text and attempts to
        making suitable replacements for the context objects

        Args:
            text: Any string that supports context expressions

        Returns:
            The resulting string after executing the context expression

        Examples:
            >>> from quilla.ctx import Context
            >>> ctx = Context(context_data={'name': 'examplesvc'})
            >>> ctx.perform_replacements('/api/${{ Validation.name }}/get')
            '/api/examplesvc/get'
        '''
        self.logger.debug('Performing replacement function on %s', text)
        while (expression_match := self._expression_regex.search(text)) is not None:
            expression = expression_match.group(1).strip()
            self.logger.debug('Found expression match: %s', expression)
            processed = self._process_objects(expression)

            self.logger.debug('Post-processing, expression value is: %s', processed)

            text = (
                text[:expression_match.start()] +
                f'{processed}' +
                text[expression_match.end():]
            )
        return text

    def _escape_quotes(self, text: str) -> str:
        return text.replace("'", "\\'")

    def _process_objects(self, expression: str) -> str:
        '''
        Performs context object replacement to ensure that the returned string is ready for
        the eval that will occur in perform_replacements

        Args:
            expression: a string that matches the _expression_regex regular expression

        Returns:
            an eval-ready string wherein all the valid context objects have been replaced
            with the appropriate values from their respective sources
        '''
        while (object_match := self._context_obj_expression.search(expression)) is not None:
            object_expression = object_match.group(0)  # Grab the full expression

            root, *path = object_expression.split('.')
            repl_value = ''

            if root == 'Environment':
                repl_value = self._escape_quotes(os.environ.get('.'.join(path), ''))
            elif root == 'Validation' or root == 'Definitions':
                data = self._context_data[root]
                data = self._walk_data_tree(data, path, object_expression)

                repl_value = cast(str, data)
            elif self.pm is not None:
                # Pass it to the defined hooks

                self.logger.debug(
                    'Context object "%s" does not match known options, forwarding to plugins',
                    root
                )

                hook_results = self.pm.hook.quilla_context_obj(
                    ctx=self,
                    root=root,
                    path=tuple(path)
                )  # type: ignore

                # Hook results will always be either size 1 or 0
                if len(hook_results) == 0:
                    repl_value = ''
                else:
                    repl_value = hook_results[0]

            if repl_value == '':
                self.logger.info(
                    'Context expression "%s" does not resolve to any value',
                    object_expression
                )

            expression = (
                expression[:object_match.start()] +
                f'{repl_value}' +
                expression[object_match.end():]
            )
        return expression

    def _walk_data_tree(self, data, exp, object_expression):
        for entry in exp:
            data = data.get(entry, None)
            if data is None:
                raise InvalidContextExpressionException(
                    f'\'{object_expression}\' does not exist'
                )
        return data

    def create_output(self, output_name: str, value: str):
        '''
        Creates an output on the context object to be returned by the validation
        module if the browser is the supported output browser, and sets the value
        in the Validation context object. Setting the value in the
        Validation context happens regardless of the browser type, since further
        steps on the validation chain could need this specific value and the order in
        which browsers are executed is dependent on the order that the user gave
        in the validation json.

        Args:
            output_name: The name (ID) of this specific output, to be referred to
                with ${{ Validation.<output_name> }}. This does support chaining of the
                namespace to create a more dictionary-like structure
            value: The value that the name will be associated with

        '''
        self.logger.debug(
            'Creating output with id "%s" and value "%s"',
            output_name,
            value,
        )
        if self.driver.name.strip().capitalize() == self._output_browser:
            self._deep_insert('Outputs', output_name, value)
        self._deep_insert('Validation', output_name, value)

    def _deep_insert(self, data_store: str, value_name: str, value: str):
        store = self._context_data[data_store]
        *name_iter, name = value_name.split('.')
        for namespace in name_iter:
            try:
                new_store = store.get(namespace, {})  # type: ignore
                store[namespace] = new_store
                store = new_store
            except Exception:
                raise InvalidOutputName(
                    f'The name \'{value_name}.{name}\' has already been used or the '
                    'namespace is invalid'
                )
        if isinstance(store, str):
            raise InvalidOutputName(
                f'The name \'{value_name}.{name}\' has already been used or the '
                'namespace is invalid'
            )

        store[name] = value  # type: ignore

    def _load_definition_files(self, definition_files: List[str]):
        '''
        Given a list of definition file names, loads all of them into the context data store
        '''
        for definition_file in definition_files:
            self.logger.info(
                'Loading definition file "%s"',
                definition_file
            )
            with open(definition_file) as fp:
                data_dict = json.load(fp)
            self.load_definitions(data_dict)

        self.logger.debug('Final Definition object: "%s"', self._context_data['Definitions'])

    def load_definitions(self, definitions_dict: dict):
        '''
        Loads the given dictionary into the context data, merging the dictionaries and preferring
        the newer configurations wherever there is a conflict

        Args:
            definitions_dict: A dictionary containing all the definitions. Definitions
                are strings saved either in an external file or in the 'definitions'
                object of the validation json that works effectively as a macro, allowing
                test writers to use declarative names for XPaths
        '''
        self._context_data['Definitions'] = pdm.deep_merge(
            self._context_data['Definitions'],
            definitions_dict
        )


def get_default_context(
        plugin_manager: PluginManager,
        debug: bool = False,
        drivers_path: str = '.',
        pretty: bool = False,
        json: str = '',
        is_file: bool = False,
        no_sandbox: bool = False,
        definitions: List[str] = [],
        recreate_context: bool = False,
        logger: Optional[Logger] = None
) -> Context:
    '''
    Gets the default context, creating a new one if necessary.

    If a context object already exists, all of the arguments passed into this function
    are ignored.

    Args:
        plugin_manager: An instance of the plugin manager class to attach to the context
        debug: Whether debug configurations should be enabled
        drivers_path: The directory holding all the required drivers
        pretty: Whether the output json should be pretty-printed
        json: The json data describing the validations
        is_file: Whether the json data was passed in originally raw or
            as a string
        no_sandbox: Specifies that Chrome and Edge should start with the --no-sandbox flag
        definitions: A list file names that contain definitions for Quilla
        recreate_context: Whether a new context object should be created or not
        logger: An optional logger instance. If None, one will be created
            with the NullHandler.

    Returns
        Application context shared for the entire application
    '''
    if Context.default_context is None or recreate_context:
        if logger is not None:
            logger.debug('Creating new default context object')

        Context.default_context = Context(
            plugin_manager,
            debug,
            drivers_path,
            pretty,
            json,
            is_file,
            no_sandbox,
            definitions,
            logger,
        )
    return Context.default_context
