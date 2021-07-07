from typing import (
    List,
    Optional,
    Dict,
    Type,
)

from selenium.webdriver.remote.webdriver import WebDriver

from quilla.ctx import Context
from quilla.common.utils import DriverHolder
from quilla.common.enums import (
    UITestActions
)
from quilla.steps.base_steps import (
    BaseStep,
    BaseStepFactory,
)
from quilla.steps.steps import TestStep
from quilla.steps.validations import Validation
from quilla.steps.outputs import OutputValueStep
from quilla.reports import (
    BaseReport,
    StepFailureReport
)


class StepsAggregator(DriverHolder):
    '''
    Test step aggregator interface. Useful for abstracting operations
    done on all the steps.
    '''
    def __init__(
        self,
        ctx: Context,
        steps: List[Dict] = [],
        driver: Optional[WebDriver] = None
    ):
        '''
        Turns an array of dictionaries into appropriate step objects, and saves them in a list
        '''

        self._steps: List[BaseStep] = []
        self._driver = driver
        self.ctx = ctx

        step_factory_selector: Dict[UITestActions, Type[BaseStepFactory]] = {
            UITestActions.VALIDATE: Validation,
            UITestActions.OUTPUT_VALUE: OutputValueStep,
        }

        # Allow plugins to add selectors
        ctx.logger.info('Running "quilla_step_factory_selector" hook')
        ctx.pm.hook.quilla_step_factory_selector(selector=step_factory_selector)

        for step in steps:
            step_factory = step_factory_selector.get(step['action'], TestStep)

            self._steps.append(step_factory.from_dict(ctx, step, driver=driver))  # type: ignore

    @property
    def driver(self) -> WebDriver:
        '''
        The webdriver attached to this object. Setting this property will also set
        the driver of all steps in the aggregator.

        Raises:
            NoDriverException: if the internal driver is currently None
        '''

        return super().driver

    @driver.setter
    def driver(self, new_driver: Optional[WebDriver]):
        for step in self._steps:
            step.driver = new_driver

        self._driver = new_driver

    def run_steps(self) -> List[BaseReport]:
        '''
        Performs all bound steps, collecting generated reports and errors

        Returns:
            A list of reports generated
        '''
        reports: List[BaseReport] = []
        for i, step in enumerate(self._steps):
            try:
                self.ctx.logger.debug('Running step %s', step.action.value)
                report = step.perform()
            except Exception as e:
                if not self.ctx.suppress_exceptions:
                    # If debugging, don't produce reports since a stack trace will be better
                    raise e

                self.ctx.logger.debug(
                    'Performing step %s caused exception %s',
                    step.action.value,
                    e,
                    exc_info=True
                )
                report = StepFailureReport(e, self.driver.name, step.action, i)
                reports.append(report)
                # Exit early, since steps producing exception can prevent future steps from working
                return reports

            if report is not None:
                reports.append(report)

        return reports

    def copy(self) -> "StepsAggregator":
        '''
        Creates a copy of the StepsAggregator object

        This is used so that each browser can have an independent copy of
        the steps, in case any script would want to edit individual browser
        steps
        '''
        steps = []

        for step in self._steps:
            steps.append(step.copy())

        duplicate = StepsAggregator(self.ctx)
        duplicate._steps = steps
        duplicate._driver = self._driver

        return duplicate
