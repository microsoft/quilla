'''
This file is used to generate the parser for the documentation. It initializes a plugin manager,
and runs the necessary hooks to set up the parser. This is done so that built-in plugins will also
appear in the usage documentation from ``doc/usage.rst``.
'''

import logging

from quilla import (
    make_parser,
)
from quilla.plugins import get_plugin_manager


def _setup_docs_parser():
    '''
    This function is deliberately not called anywhere, and will not show up
    in the documentation.
    '''
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

    parser = make_parser()
    pm = get_plugin_manager('.', logger)

    pm.hook.quilla_addopts(parser=parser)

    return parser
