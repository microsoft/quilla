from unittest.mock import Mock
from logging import (
    Logger,
    NullHandler,
)

import pytest
from _pytest.config import PytestPluginManager
from _pytest.config import Config
from selenium.webdriver.remote.webdriver import WebDriver

from quilla import get_plugin_manager
from quilla.ctx import Context
from pytest_quilla.pytest_classes import (
    collect_file
)


@pytest.fixture()
def ctx(driver: WebDriver, plugin_manager):
    '''
    Ensures every test that requires a context gets its own isolated context
    '''
    mock_ctx = Context(plugin_manager)
    driver.name = mock_ctx._output_browser
    mock_ctx.driver = driver
    return mock_ctx


@pytest.fixture()
def plugin_manager(pytestconfig: Config):
    logger = Logger('quilla-test-logger')
    logger.addHandler(NullHandler())
    pm = get_plugin_manager(str(pytestconfig.rootpath), logger)

    return pm


@pytest.fixture()
def driver():
    mock_driver = Mock(spec=WebDriver)

    return mock_driver


def pytest_addoption(parser, pluginmanager: PytestPluginManager):
    pluginmanager.set_blocked('quilla')
    parser.addoption(
        "--quilla-opts",
        action="store",
        default="",
        help="Options to be passed through to the quilla runtime for the scenario tests"
    )


def pytest_collect_file(parent, path):
    return collect_file(parent, path, 'test')
