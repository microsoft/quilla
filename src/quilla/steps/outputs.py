from typing import (
    Optional,
    Dict,
    Any
)

from selenium.webdriver.remote.webdriver import WebDriver
from quilla.common.enums import UITestActions

from quilla.ctx import Context
from quilla.common.enums import (
    OutputSources
)
from quilla.steps.base_steps import (
    BaseStep,
    BaseStepFactory
)


class OutputValueStep(BaseStep, BaseStepFactory):
    required_params = [
        'target',
        'parameters'
    ]

    @classmethod
    def from_dict(
        cls,
        ctx: Context,
        action_dict: Dict,
        driver: Optional[WebDriver] = None
    ) -> "BaseStep":
        '''
        Factory method to extract needed parameters from a dictionary
        '''
        for item in cls.required_params:
            if item not in action_dict:
                raise AttributeError('Missing one or more required parameters')

        params: Dict[str, Any] = {}

        for param in cls.required_params:
            params[param] = action_dict[param]

        return OutputValueStep(ctx, **params, driver=driver)

    def __init__(
        self,
        ctx: Context,
        target: Optional[str] = None,
        parameters: Optional[dict] = None,
        driver: Optional[WebDriver] = None,
    ):
        super().__init__(ctx, UITestActions.OUTPUT_VALUE, target, parameters, driver=driver)
        self._verify_target()
        self._verify_parameters('source', 'outputName')

        self.selector = {
            OutputSources.LITERAL: self._output_literal,
            OutputSources.XPATH_TEXT: self._output_xpath_text,
            OutputSources.XPATH_PROPERTY: self._output_xpath_property,
        }

    def perform(self):
        self.ctx.logger.debug(
            'Creating value output with source %s and target %s',
            self._parameters['source'],
            self._target,
        )
        value_producer = self.selector[self.parameters['source']]

        output_value = value_producer()
        self._create_output(output_value)

    def _create_output(self, value):
        self.ctx.create_output(self.parameters['outputName'], value)

    def _output_literal(self):
        return self.target

    def _output_xpath_text(self):
        return self.element.text

    def _output_xpath_property(self):
        self._verify_parameters('propertyName')
        property_name = self.parameters['propertyName']

        return self.element.get_property(property_name)

    def copy(self) -> "OutputValueStep":
        '''
        Creates a shallow copy of the OutputValueStep object

        This is used so that each browser can have an independent copy of
        the steps, in case any script would want to edit individual browser
        steps
        '''
        return OutputValueStep(
            self.ctx,
            self._target,      # Make sure it's passed in raw
            self._parameters,  # Make sure it's passed in raw
            self._driver
        )
