import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from pytest_quilla.pytest_classes import collect_file


def pytest_addoption(parser: Parser):
    '''
    Adds quilla INI option for enabling
    '''
    parser.addini(
        'use-quilla',
        'Enables or disables the use of Quilla for pytest',
        type='bool',
        default=False
    )
    parser.addini(
        'quilla-prefix',
        'Prefix that JSON files should have to be considered quilla test files',
        type='string',
        default='quilla'
    )


def pytest_load_initial_conftests(early_config: Config, parser: Parser):
    if not early_config.getini('use-quilla'):
        early_config.pluginmanager.set_blocked('quilla')
        return

    parser.addoption(
        "--quilla-opts",
        action="store",
        default="",
        help="Options to be passed through to the quilla runtime for the scenario tests"
    )


def pytest_collect_file(parent: pytest.Session, path):
    return collect_file(parent, path, parent.config.getini('quilla-prefix'))
