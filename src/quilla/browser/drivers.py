'''
Module for webdriver subclasses that configure the browsers
'''

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

from quilla.ctx import Context


class FirefoxBrowser(webdriver.Firefox):
    '''
    A class used to configure the Firefox browser driver for use in UIValidation module.

    Args:
        ctx: The runtime context for the application
    '''
    def __init__(self, ctx: Context):
        options = webdriver.FirefoxOptions()

        # If debugging, do not start browser in headless mode
        if ctx.run_headless:
            options.add_argument('-headless')

        super().__init__(options=options)


class ChromeBrowser(webdriver.Chrome):
    '''
    A class used to configure the Chrome browser driver for use in UIValidation module.

    Args:
        ctx: The runtime context for the application
    '''
    def __init__(self, ctx: Context):
        options = webdriver.ChromeOptions()

        if ctx.no_sandbox:
            options.add_argument('--no-sandbox')
        if ctx.run_headless:
            options.add_argument('--headless')

        super().__init__(options=options)


class EdgeBrowser(Edge):
    '''
    A class used to configure the Edge browser driver for use in UIValidation module.

    Args:
        ctx: The runtime context for the application
    '''
    def __init__(self, ctx: Context):
        options = EdgeOptions()

        options.use_chromium = True
        options.set_capability('platform', 'ANY')  # Prevent Edge from defaulting to Windows

        if ctx.no_sandbox:
            options.add_argument('--no-sandbox')
        if ctx.run_headless:
            options.add_argument('--headless')

        super().__init__(options=options)
