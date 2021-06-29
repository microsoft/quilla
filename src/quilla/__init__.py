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

from quilla.ui_validation import UIValidation
from quilla.ctx import (
    Context,
    get_default_context
)
from quilla.plugins import get_plugin_manager


def make_parser() -> argparse.ArgumentParser:  # pragma: no cover
    '''
    Creates the required parser to run UIValidation from the command line


    Returns:
        A pre-configured ArgParser instance
    '''
    parser = argparse.ArgumentParser(
        prog='quilla',
        description='''
        Program to provide a report of UI validations given a json representation
        of the validations or given the filename containing a json document describing
        the validations
        '''
    )

    parser.add_argument(
        '-f',
        '--file',
        dest='is_file',
        action='store_true',
        help='Whether to treat the argument as raw json or as a file',
    )
    parser.add_argument(
        'json',
        help='The json file name or raw json string',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="Enable debug mode",
    )
    parser.add_argument(
        '--driver-dir',
        dest="drivers_path",
        action='store',
        default='.',
        help='The directory where browser drivers are stored',
    )
    parser.add_argument(
        '-P',
        '--pretty',
        action='store_true',
        help='Set this flag to have the output be pretty-printed'
    )
    parser.add_argument(
        '--no-sandbox',
        dest='no_sandbox',
        action='store_true',
        help='''
        Adds \'--no-sandbox\' to the Chrome and Edge browsers.
        Useful for running in docker containers'
        '''
    )
    parser.add_argument(
        '-d',
        '--definitions',
        action='append',
        metavar='file',
        help='A file with definitions for the \'Definitions\' context object'
    )

    return parser


def execute(ctx: Context, json_data: str) -> int:
    '''
    Runs all defined UI validations from the json, either from file or from raw json text, and
    prints all the resulting reports to the console

    Args:
        json: The json string describing the validation

    Returns:
        Status code for the execution of the UIValidation module, determined by whether or not
        there were any reports that were flagged as failed
    '''

    ui_validation = UIValidation.from_json(ctx, json_data)

    ctx.pm.hook.quilla_prevalidate(validation=ui_validation)

    reports = ui_validation.validate_all()

    ctx.pm.hook.quilla_postvalidate(ctx=ctx, reports=reports)

    out = reports.to_dict()
    if ctx._context_data['Outputs']:
        out['Outputs'] = ctx._context_data['Outputs']

    if ctx.pretty:
        print(json.dumps(
            out,
            indent=ctx.pretty_print_indent,
            sort_keys=True
        ))
    else:
        print(json.dumps(out))

    if reports.fails > 0:
        return 1
    return 0


def setup_context(args: List[str], plugin_root: str = '.') -> Context:
    '''
    Starts up the plugin manager, creates parser, parses args and sets up the application context

    Args:
        args: A list of cli options, such as sys.argv[1:]
        plugin_root: The directory used by the plugin manager to search for `uiconf.py` files
    Returns:
        A runtime context configured by the hooks and the args
    '''
    pm = get_plugin_manager(plugin_root)
    parser = make_parser()
    pm.hook.quilla_addopts(parser=parser)  # type: ignore

    parsed_args = parser.parse_args(args)

    # Set to empty list since argparse defaults to None
    if not parsed_args.definitions:
        parsed_args.definitions = []

    if not parsed_args.is_file:
        json_data = parsed_args.json
    else:
        with open(parsed_args.json) as f:
            json_data = f.read()
    ctx = get_default_context(
        pm,
        parsed_args.debug,
        parsed_args.drivers_path,
        parsed_args.pretty,
        json_data,
        parsed_args.is_file,
        parsed_args.no_sandbox,
        parsed_args.definitions,
    )

    pm.hook.quilla_configure(ctx=ctx, args=args)

    return ctx


def run():
    '''
    Creates the parser object, parses the command-line arguments, and runs them, finishing with the
    appropriate exit code.
    '''
    ctx = setup_context(sys.argv[1:])

    exit_code = execute(ctx, ctx.json)

    sys.exit(exit_code)


if __name__ == '__main__':
    run()
