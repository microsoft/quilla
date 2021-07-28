'''
This module contains a class definition for the VisualParityValidation class, which
contains all the logic for the VisualParity validation state. Although VisualParity
is not a validation type on its own (it is a subset of XPath validations), it has particular
idiosyncracies that make more sense to have a dedicated space to handle instead of inflating
the XPathValidation class further.

This module is then used by the XPathValidation class to perform the VisualParity validation
'''

from io import BytesIO
from typing import (
    Optional,
    Tuple,
)
from math import (
    ceil,
    floor,
)

from PIL import Image
from selenium.webdriver.remote.webelement import WebElement

from quilla.ctx import Context
from quilla.reports import (
    VisualParityReport,
    ValidationReport
)
from quilla.common.enums import (
    VisualParityImageType,
    UITestActions,
)
from quilla.common.exceptions import FailedStepException

from quilla.steps.base_steps import BaseStep


class VisualParityState(BaseStep):
    '''
    Helper class to logically group methods and helper functions for VisualParity
    validation state. It inherits from BaseStep as BaseStep contains a lot of useful
    methods and properties.
    '''

    def __init__(
        self,
        ctx: Context,
        target: str,
        parameters: dict,
    ):
        super().__init__(
            ctx=ctx,
            action_type=UITestActions.VALIDATE,
            target=target,
            parameters=parameters
        )

        self._verify_parameters('baselineID')
        self.baseline_id = parameters['baselineID']
        self._driver = ctx.driver

    def copy(self):
        return VisualParityState(self.ctx, self._target, self._parameters)

    @property
    def hook(self):
        '''
        Pass-through property to make it easier to call hooks
        '''
        return self.ctx.pm.hook

    def _create_report(
        self,
        success: bool,
        msg: str = '',
        baseline_image_uri: str = '',
        treatment_image_uri: str = '',
    ) -> VisualParityReport:
        return VisualParityReport(
            success=success,
            target=self.target,
            browser_name=self.ctx.driver.name,
            baseline_id=self.baseline_id,
            msg=msg,
            baseline_image_uri=baseline_image_uri,
            treatment_image_uri=treatment_image_uri
        )

    def _update_baseline(self):

        baseline_bytes = self.element.screenshot_as_png
        baseline_image = Image.open(BytesIO(baseline_bytes))

        self.perform_exclusions(baseline_image)

        baseline_bytes = self._get_image_bytes(baseline_image)

        image_uri = self.hook.quilla_store_image(
            ctx=self.ctx,
            baseline_id=self.baseline_id,
            image_bytes=baseline_bytes,
            image_type=VisualParityImageType.BASELINE
        )

        if image_uri is None:
            return self._no_storage_mechanism_report

        if image_uri == '':
            return self._create_report(
                success=False,
                msg='Unable to update the baseline image'
            )

        return self._create_report(
            success=True,
            baseline_image_uri=image_uri,
            msg='Successfully updated baseline URI'
        )

    @property
    def _no_storage_mechanism_report(self):
        return self._create_report(
            success=False,
            msg='No baseline storage mechanism configured',
        )

    def _get_image_bytes(self, image: Image.Image):
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        return buffer.getvalue()

    def perform_exclusions(self, image: Image.Image):
        '''
        Using the 'excludeXPaths' parameter, grabs all the necessary elements
        that should be excluded, and removes them from the screenshot by covering
        the element position with a black box that is of the same size as the
        bounding box of that element.

        This mutates the original image, so nothing is returned

        Args:
            image: The image to perform the exclusions on
        '''

        exclusion_xpaths = self._parameters.get('excludeXPaths', [])

        for xpath in exclusion_xpaths:
            self._exclude_element_from_image(image, xpath)

    def _exclude_element_from_image(self, image: Image.Image, exclude_target: str):
        resolved_exclusion_target = self.ctx.perform_replacements(exclude_target)
        exclude_element = self.driver.find_element_by_xpath(resolved_exclusion_target)

        if not self._verify_exclude_target_within_bounding_box(exclude_element):
            raise FailedStepException(
                'Exclusion target element %s is not within the bounding box of %s' % (
                    exclude_target, self._target
                )
            )

        pos = self._get_element_location(exclude_element)
        size = self._get_element_size(exclude_element)

        censor_image = Image.new(image.mode, size)

        image.paste(censor_image, pos)

    def _get_element_bbox(self, element: WebElement) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        '''
        Given a web element, calculates its bounding box

        Args:
            element: A web element retrieved by Selenium

        Returns:
            A pair of tuples representing the bottom left and top right corners of the bounding box
        '''
        x, y = self._get_element_location(element)
        width, height = self._get_element_size(element)

        top_left = (x, y)
        bottom_right = (x + width, y + height)

        return top_left, bottom_right

    def _get_element_size(self, element: WebElement) -> Tuple[int, int]:
        '''
        Gets the given element integer size

        Args:
            element: A web element retrieved by Selenium

        Returns:
            A (width, height) integer tuple describing the size of the element
        '''

        size = element.size
        width = ceil(size['width'])
        height = ceil(size['height'])

        return (width, height)

    def _get_element_location(self, element: WebElement) -> Tuple[int, int]:
        '''
        Gets the integer location of the given element

        Args:
            element: A web element retrieved by Selenium

        Returns:
            A (x, y) integer tuple describing the location of the element
        '''
        loc = element.location

        x = floor(loc['x'])
        y = floor(loc['y'])

        return (x, y)

    def _verify_exclude_target_within_bounding_box(self, exclude_element: WebElement) -> bool:
        '''
        Ensures that the XPath specified is within the actual bounding box of the
        current element target.

        Note, this will return False if the XPath is only partially within the bounding
        box of the target.

        Args:
            exclude_target: The web element that should be excluded

        Returns:
            True if the element is within the target bounding box, False otherwise.
        '''
        exclude_left, exclude_right = self._get_element_bbox(exclude_element)
        target_left, target_right = self._get_element_bbox(self.element)

        bottom_contained = target_left[0] <= exclude_left[0] and target_left[1] <= exclude_left[1]
        top_contained = exclude_right[0] <= target_right[0] and exclude_right[1] <= target_right[1]

        return bottom_contained and top_contained

    def perform(self) -> ValidationReport:
        self._verify_parameters('baselineID')

        baseline_id = self.parameters['baselineID']
        update_baseline = (
            self.ctx.update_all_baselines or
            baseline_id in self.ctx.update_baseline
        )

        if update_baseline:
            return self._update_baseline()

        treatment_image_bytes = self.element.screenshot_as_png
        treatment_image = Image.open(BytesIO(treatment_image_bytes))
        treatment_image.load()  # Make sure the image is actually loaded

        self.perform_exclusions(treatment_image)

        treatment_image_bytes = self._get_image_bytes(treatment_image)

        baseline_image_bytes: Optional[bytes] = self.hook.quilla_get_visualparity_baseline(
            ctx=self.ctx,
            baseline_id=baseline_id
        )

        if baseline_image_bytes is None:
            return self._no_storage_mechanism_report

        if baseline_image_bytes == b'':
            if self.ctx.create_baseline_if_none:
                return self._update_baseline()

            return self._create_report(
                success=False,
                msg='No baseline image found'
            )

        baseline_image = Image.open(BytesIO(baseline_image_bytes))
        baseline_image.load()  # Make sure the image is actualy loaded

        success = baseline_image == treatment_image  # Run the comparison with Pillow

        if success:
            return self._create_report(
                success=success,
            )

        treatment_uri = self.hook.quilla_store_image(
            ctx=self.ctx,
            baseline_id=baseline_id,
            image_bytes=treatment_image_bytes,
            image_type=VisualParityImageType.TREATMENT,
        )

        baseline_uri = self.hook.quilla_get_baseline_uri(
            ctx=self.ctx,
            run_id=self.ctx.run_id,
            baseline_id=baseline_id
        )

        return self._create_report(
            success=False,
            baseline_image_uri=baseline_uri,
            treatment_image_uri=treatment_uri,
        )
