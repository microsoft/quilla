from typing import (
    List,
    Type,
    Dict
)
import json

from quilla.ctx import Context
from quilla.common.enums import (
    BrowserTargets,
    UITestActions,
    URLValidationStates,
    ValidationStates,
    ValidationTypes,
    XPathValidationStates,
    OutputSources
)
from quilla.steps.steps_aggregator import StepsAggregator
from quilla.browser.browser_validations import BrowserValidations
from quilla.reports import (
    BaseReport,
    ReportSummary,
)
from quilla.common.utils import EnumResolver


# All UI Validations
class QuillaTest(EnumResolver):
    '''
    A class to convert data into a valid QuillaTest instance, which is able to resolve
    raw text data into the appropriate enums to be used by the internal classes.

    Creates shallow copies of all the steps to ensure independence

    Args:
        ctx: The runtime context for the application
        browsers: A list of browsers to run the validations against
        root: The starting path of the validations
        setup_steps: a list of steps used to create the validation report

    Attributes:
        browsers: A list of instantiated browser validations, each containing an
            independent steps aggregator
        ctx: The runtime context for the application
    '''
    validation_type_selector: Dict[ValidationTypes, Type[ValidationStates]] = {
        ValidationTypes.XPATH: XPathValidationStates,
        ValidationTypes.URL: URLValidationStates,
    }

    @classmethod
    def from_json(cls, ctx: Context, validation_json: str) -> "QuillaTest":  # pragma: no cover
        '''
        Converts a json string into a UIValidation object
        '''
        return QuillaTest.from_dict(ctx, json.loads(validation_json))

    @classmethod
    def from_file(cls, ctx: Context, fp) -> "QuillaTest":  # pragma: no cover
        '''
        Converts an fp (a .read() supporting file-like object) containing a json
        document into a UIValidation object
        '''
        return QuillaTest.from_dict(ctx, json.load(fp))

    @classmethod
    def from_filename(cls, ctx: Context, path: str) -> "QuillaTest":  # pragma: no cover
        '''
        Reads a file at the specified path and attempts to convert it into a
        UIValidation object
        '''
        with open(path) as fp:
            return QuillaTest.from_file(ctx, fp)

    @classmethod
    def from_dict(cls, ctx: Context, validation_parameters: dict) -> "QuillaTest":
        '''
        Converts a dictionary that represents a single UIValidation test case into
        the appropriate validation object.

        Note:
            The browsers are effectively a cartesian product with the steps & validations
        '''
        root_path: str = validation_parameters['path']

        definitions = validation_parameters.get('definitions', {})

        ctx.logger.debug('Validation included definitions: %s', definitions)

        ctx.load_definitions(definitions)

        browsers: List[BrowserTargets] = []
        for browser_name in validation_parameters['targetBrowsers']:
            browsers.append(cls._name_to_enum(browser_name, BrowserTargets, ctx=ctx))

        steps = validation_parameters['steps']

        for step in steps:
            ctx.logger.debug('Processing step %s', step)

            action = step['action']
            action = cls._name_to_enum(action, UITestActions)
            step['action'] = action
            if action == UITestActions.VALIDATE:
                validation_type = step['type']
                validation_state = step['state']

                validation_type = cls._name_to_enum(validation_type, ValidationTypes, ctx=ctx)

                state_enum = cls.validation_type_selector[validation_type]

                validation_state = cls._name_to_enum(validation_state, state_enum, ctx=ctx)

                step['type'] = validation_type
                step['state'] = validation_state

            if 'parameters' in step:
                params = step['parameters']
                if 'source' in params:
                    source = params['source']
                    params['source'] = cls._name_to_enum(source, OutputSources, ctx=ctx)
                step['parameters'] = params

        return QuillaTest(
            ctx,
            browsers,
            root_path,
            steps,
        )

    def __init__(
        self,
        ctx: Context,
        browsers: List[BrowserTargets],
        root: str,
        setup_steps: list,
    ):
        self.ctx = ctx
        self._steps = steps = StepsAggregator(ctx, setup_steps)

        self.browsers: List[BrowserValidations] = []

        for browser_target in browsers:
            self.browsers.append(
                BrowserValidations(
                    ctx,
                    browser_target,
                    root,
                    steps.copy(),
                )
            )

    def validate_all(self) -> ReportSummary:
        '''
        Performs all the setup test steps required for each test case
        and executes the validations, producing a set of validation
        reports.
        '''
        validation_reports: List[BaseReport] = []
        for browser in self.browsers:
            validation_reports.extend(browser.validate())

        return ReportSummary(validation_reports)
