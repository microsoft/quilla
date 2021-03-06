import re
from typing import (
    Optional,
    Dict,
    Callable,
    List
)

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from quilla.ctx import Context
from quilla.common.enums import (
    XPathValidationStates,
    ValidationStates,
    ValidationTypes,
)
from quilla.reports import (
    ValidationReport,
)
from quilla.steps.base_steps import BaseValidation
from quilla.steps.validations.visual_parity import VisualParityState


class XPathValidation(BaseValidation):
    '''
    Class defining the behaviour for performing XPath validations

    Args:
        ctx: The runtime context for the application
        target: The XPath of the element to perform the validation against
        state: The desired state of the target web element
        driver: An optional argument to allow the driver to be bound at object creation.
    '''
    def __init__(
        self,
        ctx: Context,
        target: str,
        state: XPathValidationStates,
        parameters: Optional[Dict],
        driver: Optional[WebDriver] = None,
    ) -> None:
        selector: Dict[ValidationStates, Callable[[], ValidationReport]] = {
            XPathValidationStates.EXISTS: self._check_exists,
            XPathValidationStates.NOT_EXISTS: self._check_not_exists,
            XPathValidationStates.VISIBLE: self._check_visible,
            XPathValidationStates.NOT_VISIBLE: self._check_not_visible,
            XPathValidationStates.TEXT_MATCHES: self._check_text_matches,
            XPathValidationStates.NOT_TEXT_MATCHES: self._check_not_text_matches,
            XPathValidationStates.HAS_PROPERTY: self._check_has_property,
            XPathValidationStates.NOT_HAS_PROPERTY: self._check_not_has_property,
            XPathValidationStates.PROPERTY_HAS_VALUE: self._check_property_has_value,
            XPathValidationStates.NOT_PROPERTY_HAS_VALUE: self._check_not_property_has_value,
            XPathValidationStates.HAS_ATTRIBUTE: self._check_has_attribute,
            XPathValidationStates.NOT_HAS_ATTRIBUTE: self._check_not_has_attribute,
            XPathValidationStates.ATTRIBUTE_HAS_VALUE: self._check_attribute_has_value,
            XPathValidationStates.NOT_ATTRIBUTE_HAS_VALUE: self._check_not_attribute_has_value,
            XPathValidationStates.VISUAL_PARITY: self._check_visual_parity,
        }
        super().__init__(
            ctx,
            ValidationTypes.XPATH,
            target,
            state,
            selector,
            parameters=parameters,
            driver=driver
        )

    def _find_all(self) -> List[WebElement]:
        '''
        Proxy method to find all elements specified by the _target attribute

        Returns:
            A list of all the elements found for that specific target, searched by XPath

        Raises:
            NoDriverException: If the driver is not currently bound to this step
        '''
        return self.driver.find_elements(By.XPATH, self.target)

    def _element_text_matches_pattern(self) -> bool:
        self._verify_parameters('pattern')
        element_text = self.element.text
        pattern = self.parameters['pattern']

        return re.search(pattern, element_text) is not None

    def _element_exists(self) -> bool:
        return len(self._find_all()) > 0

    def _element_visible(self) -> bool:
        return self.element.is_displayed()

    def _element_has_property(self) -> bool:
        self._verify_parameters('name')

        return self.element.get_property(self.parameters['name']) is not None

    def _element_has_attribute(self) -> bool:
        self._verify_parameters('name')

        return self.element.get_attribute(self.parameters['name']) is not None

    def _element_check_value(self, value_fetch_fn: Callable[[str], Optional[str]]) -> bool:
        self._verify_parameters('name', 'value')

        element_value = value_fetch_fn(self.parameters['name'])

        return element_value == self.parameters['value']

    def _element_property_has_value(self) -> bool:
        return self._element_check_value(self.element.get_property)

    def _element_attribute_has_value(self) -> bool:
        return self._element_check_value(self.element.get_attribute)

    def _check_exists(self) -> ValidationReport:
        return self._create_report(
            self._element_exists()
        )

    def _check_not_exists(self) -> ValidationReport:
        return self._create_report(
            not self._element_exists
        )

    def _check_visible(self) -> ValidationReport:
        return self._create_report(
            self._element_visible()
        )

    def _check_not_visible(self) -> ValidationReport:
        return self._create_report(
            not self._element_visible
        )

    def _check_text_matches(self) -> ValidationReport:
        text_matches = self._element_text_matches_pattern()
        msg = ''

        if not text_matches:
            msg = (
                f'Element text "{self.element.text}" '
                f'does not match pattern "{self._parameters["pattern"]}"'
            )
        return self._create_report(
            text_matches,
            msg
        )

    def _check_not_text_matches(self) -> ValidationReport:
        text_matches = self._element_text_matches_pattern()
        msg = ''

        if text_matches:
            msg = (
                f'Element text "{self.element.text}" '
                f'matches pattern "{self._parameters["pattern"]}"'
            )
        return self._create_report(
            not text_matches,
            msg
        )

    def _check_has_property(self) -> ValidationReport:
        return self._create_report(
            self._element_has_property()
        )

    def _check_not_has_property(self) -> ValidationReport:
        return self._create_report(
            not self._element_has_property()
        )

    def _check_has_attribute(self) -> ValidationReport:
        return self._create_report(
            self._element_has_attribute()
        )

    def _check_not_has_attribute(self) -> ValidationReport:
        return self._create_report(
            not self._element_has_attribute()
        )

    def _check_property_has_value(self) -> ValidationReport:
        return self._create_report(
            self._element_property_has_value()
        )

    def _check_not_property_has_value(self) -> ValidationReport:
        return self._create_report(
            not self._element_property_has_value()
        )

    def _check_attribute_has_value(self) -> ValidationReport:
        return self._create_report(
            self._element_attribute_has_value()
        )

    def _check_not_attribute_has_value(self) -> ValidationReport:
        return self._create_report(
            not self._element_attribute_has_value
        )

    def _check_visual_parity(self) -> ValidationReport:
        visual_parity = VisualParityState(
            self.ctx,
            self._target,
            self._parameters
        )

        return visual_parity.perform()
