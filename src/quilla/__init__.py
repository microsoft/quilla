'''
Entrypoint code for the Quilla module. Deals with setting up the parser and
the runtime context for the application, then executing the rest of the application
'''
import argparse
import sys
import json
from typing import (
    List,
)
import logging
from pkg_resources import get_distribution

from quilla.ui_validation import QuillaTest
from quilla.ctx import (
    Context,
    get_default_context
)
from quilla.reports import ReportSummary
from quilla.plugins import get_plugin_manager


def make_parser() -> argparse.ArgumentParser:  # pragma: no cover
    '''
    Creates the required parser to run Quilla from the command line


    Returns:
        A pre-configured ArgParser instance
    '''
    parser = argparse.ArgumentParser(
        prog='quilla',
        description='''
        Program to provide a report of UI validations given a json representation
        of the validations or given the filename containing a json document describing
        the validations
        ''',
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Prints the version of the software and quits'
    )

    data_group = parser.add_mutually_exclusive_group()

    data_group.add_argument(
        '-f',
        '--file',
        dest='file_name',
        action='store',
        help='A file containing a Quilla test',
        default=None,
    )
    data_group.add_argument(
        '-r',
        '--raw',
        action='store',
        help='A Quilla test passed in as a raw string',
        default=None,
    )

    config_group = parser.add_argument_group(title='Configuration options')
    config_group.add_argument(
        '-i',
        '--run-id',
        action='store',
        metavar='run_id',
        default=None,
        help='A run ID for quilla, if manually passed in. '
        'Used to set many quilla tests to have the same run ID '
        'If no run ID is manually passed in, it will be auto-generated'
    )
    config_group.add_argument(
        '-u',
        '--update-baseline',
        dest='update_baseline',
        action='append',
        metavar='BASELINE_ID',
        help='Used to update the specific baseline image associated with '
        'the provided baseline ID for VisualParity. '
        'Different plugins define different behaviour, so this is not '
        'necessarily a lossless operation.',
        default=[],
    )
    config_group.add_argument(
        '-U',
        '--update-all-baselines',
        dest='update_all_baselines',
        action='store_true',
        help='Used to update all baseline images in a Quilla test file. '
        'this is equivalent to using --update-baseline with every baseline ID '
        'that is used in the Quilla test.'
    )
    config_group.add_argument(
        '--create-baseline-if-absent',
        dest='create_baseline_if_none',
        action='store_true',
        help='A flag to set that will create a new baseline image if a storage '
        'mechanism is configured but no baseline image is found with the specified ID.'
    )
    config_group.add_argument(
        '-d',
        '--definitions',
        action='append',
        metavar='file',
        help='A file with definitions for the \'Definitions\' context object'
    )
    config_group.add_argument(
        '--driver-dir',
        dest='drivers_path',
        action='store',
        default='.',
        help='The directory where browser drivers are stored',
    )
    config_group.add_argument(
        '--no-sandbox',
        dest='no_sandbox',
        action='store_true',
        help='''
        Adds \'--no-sandbox\' to the Chrome and Edge browsers.
        Useful for running in docker containers'
        '''
    )

    output_group = parser.add_argument_group(title='Output Options')
    output_group.add_argument(
        '-P',
        '--pretty',
        action='store_true',
        help='Set this flag to have the output be pretty-printed'
    )
    output_group.add_argument(
        '--indent',
        type=int,
        default=4,
        help='How much space each indent level should have when pretty-printing the report'
    )

    debug_group = parser.add_argument_group(title='Debug Options')
    debug_group.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode',
    )
    debug_group.add_argument(
        '-v',
        '--verbose',
        action='count',
        help='Flag to increase the verbosity of the outputs. '
        'Log outputs are directed to stderr by default.',
        default=0
    )

    # Sets the application handler, i.e. the function that runs when ctx.run() is called
    parser.set_defaults(handler=run)

    return parser


def get_early_configs(parser: argparse.ArgumentParser, args: List[str]) -> argparse.Namespace:
    '''
    Extracts known configs early on. This will disable help/usage printing and prevent
    exiting on failure, since it potentially needs to ignore errors to collect the early configs

    Args:
        parser: A parser instance, such as the one returned by `make parser`
        args: A list of strings containing the arguments to be consumed

    Returns:
        A namespace object containing the early configurations for Quilla

    '''

    # Saves functions that need to be disabled for early configs
    exit_function = parser.exit
    print_help_fn = parser.print_help
    print_usage_fn = parser.print_usage

    # "Disable" the above functions
    do_nothing = lambda *x: None  # noqa: E731
    parser.exit = do_nothing  # type: ignore
    parser.print_help = do_nothing  # type: ignore
    parser.print_usage = do_nothing  # type: ignore

    # Get early args
    parsed_args, _ = parser.parse_known_intermixed_args(args)

    # Revert the disabled functions to their normal usage
    parser.exit = exit_function  # type: ignore
    parser.print_help = print_help_fn  # type: ignore
    parser.print_usage = print_usage_fn  # type: ignore

    return parsed_args


def make_default_logger(early_configs: argparse.Namespace) -> logging.Logger:
    '''
    Creates a default logger class for Quilla. All internal logger setup logic
    is done in this function

    Args:
        early_configs: The extracted configurations from an early pass-through
            of the parse_known_intermixed_args function, before plugins run

    Returns:
        A configured ``Logger``
    '''
    logger = logging.getLogger('quilla')

    logger.propagate = False  # Disable the root logger

    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] - %(message)s',
        datefmt='%H:%M:%S'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    if early_configs.verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif early_configs.verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)

    if early_configs.debug:
        logger.setLevel(logging.DEBUG)

    return logger


def execute(ctx: Context) -> ReportSummary:
    '''
    Runs all defined UI validations from the json, either from file or from raw json text, and
    prints all the resulting reports to the console

    Args:
        json: The json string describing the validation

    Returns:
        A summary of all reports produced by Quilla
    '''

    ctx.logger.debug('Building UIValidation object from JSON')
    quilla_test = QuillaTest.from_json(ctx, ctx.json)

    ctx.logger.info('Passing UIValidation instance to "quilla_prevalidate" hook')
    ctx.pm.hook.quilla_prevalidate(validation=quilla_test)

    ctx.logger.debug('Running all validations')
    reports = quilla_test.validate_all()

    ctx.logger.info('Running "quilla_postvalidate" hooks')
    ctx.pm.hook.quilla_postvalidate(ctx=ctx, reports=reports)

    return reports


def setup_context(
    args: List[str],
    plugin_root: str = '.',
    recreate_context: bool = False,
) -> Context:
    '''
    Starts up the plugin manager, creates parser, parses args and sets up the application context

    Args:
        args: A list of cli options, such as sys.argv[1:]
        plugin_root: The directory used by the plugin manager to search for `uiconf.py` files
        recreate_context: Whether the context should be recreated
    Returns:
        A runtime context configured by the hooks and the args
    '''
    parser = make_parser()
    early_configs = get_early_configs(parser, args)

    if early_configs.version:
        print(f'Quilla v{get_distribution("quilla").version}')
        sys.exit(0)

    logger = make_default_logger(early_configs)

    logger.debug('Default logger configured, running Quilla with args %s', args)

    logger.debug('Initializing plugin manager')

    pm = get_plugin_manager(plugin_root, logger)

    logger.info('Running "quilla_configure_logger" hook')
    pm.hook.quilla_configure_logger(logger=logger)

    logger.info('Running "quilla_addopts" hook')
    pm.hook.quilla_addopts(parser=parser)  # type: ignore

    logging.debug('Parsing all args')
    parsed_args = parser.parse_args(args)

    # Set to empty list since argparse defaults to None
    if not parsed_args.definitions:
        parsed_args.definitions = []

    if parsed_args.file_name is None:
        json_data = parsed_args.raw
    else:
        with open(parsed_args.file_name) as f:
            json_data = f.read()

    logger.debug('Initializing context object')

    ctx = get_default_context(
        pm,
        parsed_args.debug,
        parsed_args.drivers_path,
        parsed_args.pretty,
        json_data,
        parsed_args.file_name is not None,
        parsed_args.no_sandbox,
        parsed_args.definitions,
        logger=logger,
        run_id=parsed_args.run_id,
        indent=parsed_args.indent,
        update_all_baselines=parsed_args.update_all_baselines,
        update_baseline=parsed_args.update_baseline,
        create_baseline_if_none=parsed_args.create_baseline_if_none,
        args=parsed_args,
        recreate_context=recreate_context,
    )

    logger.info('Running "quilla_configure" hook')
    pm.hook.quilla_configure(ctx=ctx, args=parsed_args)

    return ctx


def run(ctx: Context):
    '''
    Runs all reports and prints to stdout while providing the proper
    exit code

    Args:
        ctx: The application context
    '''
    reports = execute(ctx)

    ctx.logger.debug('Finished generating reports')

    out = reports.to_dict()

    if ctx.pretty:
        print(json.dumps(
            out,
            indent=ctx.pretty_print_indent,
            sort_keys=True
        ))
    else:
        print(json.dumps(out))

    if reports.fails > 0:
        exit_code = 1
    else:
        exit_code = 0

    sys.exit(exit_code)


def main():
    '''
    Creates the context and parses all arguments, then runs the default handler function
    '''
    ctx = setup_context(sys.argv[1:])
    ctx.logger.debug('Context setup complete, running the Quilla handler')

    ctx.run()


if __name__ == '__main__':
    main()
