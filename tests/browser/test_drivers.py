import pytest

from quilla.ctx import Context
from quilla.browser.drivers import (
    FirefoxBrowser
)


@pytest.mark.browser
@pytest.mark.firefox
@pytest.mark.slow
class FirefoxBrowserTests:
    def test_runs_headless(self, ctx: Context):
        '''
        Only test that the default behaviour is to run headless, since the testing environment
        might not support a display
        '''
        browser = FirefoxBrowser(ctx)

        assert browser.capabilities['moz:headless'] is True

        browser.quit()
