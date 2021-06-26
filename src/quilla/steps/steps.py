'''
Module containing all the requisite classes to perform test steps.

Adding new actions
-------------------

Creating new simple actions in the code is designed to be fairly straightforward, and only
requires three steps:

1. Add an entry for the action on the ``enums`` module
2. Create a function to perform the actual step under the ``TestStep`` class
3. Add an entry to the selector with the enum as a key and the function as a value

Keep in mind that the step function should also validate any required data, and that
updating the schema for proper json validation is essential.

If the parameters for the new action are expected to be enums, you must also add the logic
for converting the parameter from string to enum in the ``UIValidation`` class.
'''


from typing import (
    Optional,
    Dict,
    Any,
)

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from quilla.ctx import Context
from quilla.common.enums import (
    UITestActions,
)
from quilla.steps.base_steps import (
    BaseStepFactory,
    BaseStep
)


# Steps classes
class TestStep(BaseStep, BaseStepFactory):
    '''
    Class that contains the definition of a single test step.
    Used for setting up validations

    Args:
        ctx: The runtime context of the application
        action: The action enum for this step
        target: What the target for this step is, if applicable
        parameters: Extra options for certain actions
        aggregator: The parent object holding this step
        driver: The browser driver

    Attributes:
        selector: A dictionary that maps action enums to the action function
    '''
    required_params = [
        'action',
    ]
    optional_params = [
        'target',
        'parameters',
    ]

    @classmethod
    def from_dict(
        cls,
        ctx: Context,
        action_dict,
        driver: Optional[WebDriver] = None
    ) -> "TestStep":
        '''
        Factory method to extract needed parameters from a dictionary
        '''
        for item in cls.required_params:
            if item not in action_dict:
                raise AttributeError('Missing one or more required parameters')

        params: Dict[str, Any] = {}

        for param in cls.required_params:
            params[param] = action_dict[param]

        for param in cls.optional_params:
            if param in action_dict:
                params[param] = action_dict[param]

        return TestStep(ctx, **params, driver=driver)

    def __init__(
        self,
        ctx: Context,
        action: UITestActions,
        target: Optional[str] = None,
        parameters: Optional[dict] = None,
        driver: Optional[WebDriver] = None,
    ):
        super().__init__(ctx, action, target=target, parameters=parameters, driver=driver)
        self.selector = {
            UITestActions.CLICK: self._click,
            UITestActions.CLEAR: self._clear,
            UITestActions.SEND_KEYS: self._send_keys,
            UITestActions.NAVIGATE_TO: self._navigate_to,
            UITestActions.WAIT_FOR_VISIBILITY: self._wait_for_visibility,
            UITestActions.WAIT_FOR_EXISTENCE: self._wait_for_existence,
            UITestActions.NAVIGATE_BACK: self._navigate_back,
            UITestActions.NAVIGATE_FORWARD: self._navigate_forward,
            UITestActions.HOVER: self._hover,
            UITestActions.REFRESH: self._refresh,
            UITestActions.SET_BROWSER_SIZE: self._set_browser_size,
            UITestActions.ADD_COOKIES: self._add_cookies,
            UITestActions.SET_COOKIES: self._set_cookies,
            UITestActions.CLEAR_COOKIES: self._clear_cookies,
            UITestActions.REMOVE_COOKIE: self._remove_cookie,
        }

    def copy(self) -> "TestStep":
        '''
        Creates a shallow copy of the TestStep object

        This is used so that each browser can have an independent copy of
        the steps, in case any script would want to edit individual browser
        steps
        '''
        return TestStep(
            self.ctx,
            self.action,
            self._target,      # Make sure it's passed in raw
            self._parameters,  # Make sure it's passed in raw
            self._driver
        )

    def perform(self):
        '''
        Runs the specified action. Wrapper for selecting proper inner method
        '''
        perform_action = self.selector[self.action]

        return perform_action()

    def _click(self):
        self._verify_target()
        self.element.click()

    def _clear(self):
        self._verify_target()
        self.element.clear()

    def _send_keys(self):
        self._verify_parameters('data')
        self.element.send_keys(self.parameters['data'])

    def _navigate_to(self):
        self._verify_target()
        self.driver.get(self.target)

    def _wait_for(self, condition):
        self._verify_parameters('timeoutInSeconds')
        WebDriverWait(self.driver, self.parameters['timeoutInSeconds']).until(condition)

    def _wait_for_visibility(self):
        self._verify_target()
        self._wait_for(EC.visibility_of_element_located(self.locator))

    def _wait_for_existence(self):
        self._verify_target()
        self._wait_for(EC.presence_of_element_located(self.locator))

    def _navigate_back(self):
        self.driver.back()

    def _navigate_forward(self):
        self.driver.forward()

    def _refresh(self):
        self.driver.refresh()

    def _set_browser_size(self):
        self._verify_parameters('width', 'height')
        width = self._parameters['width']
        height = self._parameters['height']
        self.driver.set_window_size(width, height)

    def _set_cookies(self):
        self._clear_cookies()
        self._add_cookies()

    def _add_cookies(self):
        self._verify_parameters('cookieJar')
        self.driver.add_cookie(self.parameters['cookieJar'])

    def _remove_cookie(self):
        self._verify_parameters('cookieName')
        self.driver.delete_cookie(self.parameters['cookieName'])

    def _clear_cookies(self):
        self.driver.delete_all_cookies()

    def _hover(self):
        self._verify_target()
        ActionChains(self.driver).move_to_element(self.element).perform()

    def _set_zoom_level(self):
        self._verify_parameters('zoomLevel')
        zoom_level = self._parameters['zoomLevel']
        self.driver.execute_script(f'document.body.style.zoom="{zoom_level}%"')
