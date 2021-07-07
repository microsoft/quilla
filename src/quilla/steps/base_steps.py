from typing import (
    Optional,
    Callable,
    Dict,
    Any,
)
from abc import abstractclassmethod, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from quilla.ctx import Context
from quilla.reports import (
    BaseReport,
    ValidationReport
)
from quilla.common.utils import (
    DriverHolder,
    EnumResolver
)
from quilla.common.enums import (
    UITestActions,
    ValidationTypes,
    ValidationStates,
)
from quilla.common.exceptions import FailedStepException


class BaseStep(DriverHolder, EnumResolver):
    '''
    Base class for all step objects

    Args:
        ctx: The runtime context for the application
        action_type: Enum defining which of the supported actions this class represents
        driver: An optional argument to allow the driver to be bound at object creation.

    Attributes:
        ctx: The runtime context for the application
        action: Enum defining which of the supported actions this class represents
    '''
    def __init__(
        self,
        ctx: Context,
        action_type: UITestActions,
        target: Optional[str] = None,
        parameters: Optional[dict] = None,
        driver: Optional[WebDriver] = None
    ):
        self.action = action_type
        self.ctx = ctx
        self.target = target
        self.parameters = parameters
        super().__init__(driver)

    @abstractmethod
    def perform(self) -> Optional[BaseReport]:  # pragma: no cover
        '''
        Runs the necessary action. If the action is a Validate action, will return a
        ValidationReport

        Returns:
            A report produced by the step, or None if no report is required
        '''
        pass

    @abstractmethod
    def copy(self) -> "BaseStep":
        '''
        Returns a copy of the current Step object
        '''

    @property
    def target(self):
        '''
        The target for an action, if applicable. Will resolve all context
        expressions before being returned
        '''
        if self._target is not None:
            return self.ctx.perform_replacements(self._target)

    @target.setter
    def target(self, val: str) -> str:
        self._target = val
        return val

    @property
    def parameters(self):
        '''
        Parameters for an action, if applicable. Will resolve all context
        expressions before being returned
        '''
        if self._parameters is not None:
            return self._deep_replace(self.ctx, self._parameters.copy())

    @parameters.setter
    def parameters(self, val: dict) -> dict:
        self._parameters = val
        return val

    def _deep_replace(self, ctx: Context, params: Dict[str, Any]):
        for key, value in params.items():
            if isinstance(value, str):
                params[key] = ctx.perform_replacements(value)
            elif isinstance(value, Dict):
                params[key] = self._deep_replace(ctx, value)
            # (TODO): Add list support to deep replacement
        return params

    def _verify_parameters(self, *parameters: str):
        for parameter in parameters:
            if parameter not in self.parameters:  # type: ignore
                raise FailedStepException(
                    f'"{parameter}" parameter not specified for "{self.action.value}" action'
                )

    def _verify_target(self):
        if self.target is None:
            raise FailedStepException(f'No specified target for "{self.action.value}" action')

    @property
    def element(self) -> WebElement:
        '''
        Located WebElement instance
        '''
        return self.driver.find_element(*self.locator)

    @property
    def locator(self):
        '''
        Locator for selenium to find web elements
        '''
        return (By.XPATH, self.target)


class BaseStepFactory:
    @abstractclassmethod
    def from_dict(cls, ctx: Context, step: Dict, driver: Optional[WebDriver] = None) -> BaseStep:
        '''
        Given a context, step dictionary, and optionally a driver, return an appropriate subclass
        of BaseStep

        Args:
            ctx: The runtime context of the application
            step: A dictionary defining the step
            driver: Optionally, a driver to bind to the resulting step

        Returns:
            The resulting step object
        '''


class BaseValidation(BaseStep):
    '''
    Base validation class with shared functionality for all validations

    Args:
        ctx: The runtime context for the application
        type_: An enum describing the type of supported validation
        target: The general target that this validation will seek. What it means is
            specific to each subclass of this class
        state: An enum describing the desired state of this validation. The specific
            enum is a subclass of the ValidationStates class specific to the subclass
            of BaseValidation being used
        selector: A dictionary that maps the state enum to the appropriate function
    '''
    def __init__(
        self,
        ctx: Context,
        type_: ValidationTypes,
        target: str,
        state: ValidationStates,
        selector: Dict[ValidationStates, Callable[[], ValidationReport]],
        parameters: Optional[Dict],
        driver: Optional[WebDriver] = None,
    ) -> None:
        super().__init__(
            ctx,
            UITestActions.VALIDATE,
            target=target,
            parameters=parameters,
            driver=driver
        )
        self._type = type_
        self._state = state
        self._driver = driver
        self._selector = selector
        self._report: Optional[ValidationReport] = None

    def copy(self) -> "BaseValidation":
        # All classes derived from BaseValidation only need these parameters
        return self.__class__(  # type: ignore
            self.ctx,  # type: ignore
            self._target,  # type: ignore
            self._state,  # type: ignore
            self._parameters,  # type: ignore
            self._driver  # type: ignore
        )

    def perform(self) -> ValidationReport:
        '''
        Performs the correct action based on what is defined within the selector,
        and returns the resulting report produced.

        Returns:
            A report summarizing the results of the executed validation
        '''
        self.ctx.logger.debug(
            'Performing %s with desired state "%s"',
            self._type.value,
            self._state.value
        )
        action_function = self._selector[self._state]
        self._report = action_function()

        return self._report

    def _create_report(self, success: bool, msg: str = "") -> ValidationReport:
        '''
        Creates a new validation report. Used to simplify the common shared
        behaviour that all validation reports require

        Args:
            success: Value representing the successfulness of the validation. True if
                the validation passed, False otherwise
            msg: An optional string message to be included in the report

        Returns:
            A report summarizing the results of the executed validation
        '''
        return ValidationReport(
            self._type.value,
            self._target,
            self._state.value,
            self.driver.name.capitalize(),
            success=success,
            msg=msg
        )
