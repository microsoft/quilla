from typing import (
    Optional,
    Dict,
    Callable,
)

from selenium.webdriver.remote.webdriver import WebDriver

from quilla.ctx import Context
from quilla.common.enums import (
    ValidationStates,
    ValidationTypes,
    URLValidationStates,
)
from quilla.reports import ValidationReport
from quilla.steps.base_steps import BaseValidation


class URLValidation(BaseValidation):
    '''
    Class defining the behaviour for performing URL validations

    Args:
        ctx: The runtime context for the application
        target: The URL to perform the validation with
        state: The desired state of the target url
        driver: An optional argument to allow the driver to be bound at object creation.
    '''
    def __init__(
        self,
        ctx: Context,
        target: str,
        state: URLValidationStates,
        parameters: Optional[Dict],
        driver: Optional[WebDriver] = None,
    ) -> None:
        selector: Dict[ValidationStates, Callable[[], ValidationReport]] = {
            URLValidationStates.CONTAINS: self._check_contains,
            URLValidationStates.NOT_CONTAINS: self._check_not_contains,
            URLValidationStates.EQUALS: self._check_equals,
            URLValidationStates.NOT_EQUALS: self._check_not_equals
        }
        super().__init__(
            ctx,
            ValidationTypes.URL,
            target,
            state,
            selector=selector,
            parameters=parameters,
            driver=driver
        )

    def perform(self) -> ValidationReport:
        '''
        Performs the correct action based on what is defined within the selector, and returns
        the resulting report produced.

        Returns:
            A report summarizing the results of the executed validation
        '''
        report = super().perform()

        if not report.success:
            report.msg = f'Expected URL: "{self._target}", Received URL "{self.url}"'

        return report

    @property
    def url(self) -> str:
        '''
        The current URL of the browser

        Raises:
            NoDriverException: If the driver is not currently bound to this step
        '''
        return self.driver.current_url

    def _check_contains(self) -> ValidationReport:
        return self._create_report(
            self.url.find(self.target) > -1
        )

    def _check_not_contains(self) -> ValidationReport:
        return self._create_report(
            self.url.find(self.target) == -1
        )

    def _check_equals(self) -> ValidationReport:
        return self._create_report(
            self.url == self.target
        )

    def _check_not_equals(self) -> ValidationReport:
        return self._create_report(
            self.url != self.target
        )
