from typing import (
    cast,
    Optional,
    Dict,
    Union,
    Type
)

from selenium.webdriver.remote.webdriver import WebDriver

from quilla.ctx import Context
from quilla.common.enums import (
    ValidationTypes,
    ValidationStates,
)
from quilla.steps.base_steps import (
    BaseStepFactory,
    BaseValidation,
)
from quilla.steps.validations.xpath import XPathValidation
from quilla.steps.validations.url import URLValidation


ValidationDictionary = Dict[str, Union[str, ValidationStates, ValidationTypes]]


class Validation(BaseStepFactory):
    '''
    Factory class for the different validations
    '''
    validation_selector: Dict[ValidationTypes, Type[BaseValidation]] = {
        ValidationTypes.XPATH: XPathValidation,
        ValidationTypes.URL: URLValidation,
    }

    @classmethod
    def from_dict(
        cls,
        ctx: Context,
        validation_dict: ValidationDictionary,
        driver: Optional[WebDriver] = None
    ) -> BaseValidation:
        '''
        From a validation dict, produces the appropriate validation object

        Args:
            ctx: The runtime context for the application
            validation_dict: A dictionary containing the definition of a validation, including
                the target, state, and type of validation to be performed
            driver: The driver that will be connected to the validation, if any

        Returns:
            Validation object of the type requested in the validation dictionary
        '''
        validation_params = {
            'driver': driver,
            'target': validation_dict['target'],
            'state': validation_dict['state'],
            'parameters': validation_dict.get('parameters', None),
        }

        validation_type = cast(ValidationTypes, validation_dict['type'])

        validation = cls.validation_selector[validation_type]

        return validation(ctx=ctx, **validation_params)  # type: ignore
