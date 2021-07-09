
from quilla.common.enums import (
    XPathValidationStates,
    ValidationTypes
)
from quilla.reports.validation_report import ValidationReport


class VisualParityReport(ValidationReport):
    '''
    Report type for VisualParity validation state

    Args:
        target: The validation target
        browser_name: The name of the browser that the validation was performed on
        success: Whether the validation passed or not
        msg: An optional string adding further context to the report
        baseline_id: The ID for the image baseline
        baseline_image_uri: A URI that allows locating the baseline image (i.e. path, link, etc)
        treatment_image_uri: A URI that allows locating the treatment image (i.e. path, link, etc)
        delta_image_uri: A URI that allows locating the delta image (i.e. path, link, etc)

    Attributes:
        validation_type: The string representation of the type of validation performed
        target: The validation target
        state: The desired state used for validation
        success: Whether the validation passed or not
        msg: An optional string adding further context to the report
        baseline_id: The ID for the image baseline
        baseline_image_uri: A URI that allows locating the baseline image (i.e. path, link, etc)
        treatment_image_uri: A URI that allows locating the treatment image (i.e. path, link, etc)
        delta_image_uri: A URI that allows locating the delta image (i.e. path, link, etc)
    '''

    def __init__(
        self,
        target: str,
        browser_name: str,
        success: bool,
        baseline_id: str,
        msg: str = '',
        baseline_image_uri: str = '',
        treatment_image_uri: str = '',
        delta_image_uri: str = '',
    ):
        super().__init__(
            validation_type=ValidationTypes.XPATH.value,
            target=target,
            state=XPathValidationStates.VISUAL_PARITY.value,
            browser_name=browser_name,
            success=success,
            msg=msg
        )
        self.baseline_id = baseline_id,
        self.baseline_image_uri = baseline_image_uri,
        self.treatment_image_uri = treatment_image_uri,
        self.delta_image_uri = delta_image_uri

    def to_dict(self):
        report = super().to_dict()

        report_data = report['validationReport']

        report_data['baselineId'] = self.baseline_id

        if self.baseline_image_uri:
            report_data['baselineImageUri'] = self.baseline_image_uri

        if self.treatment_image_uri:
            report_data['treatmentImageUri'] = self.treatment_image_uri

        if self.delta_image_uri:
            report_data['deltaImageUri'] = self.delta_image_uri

        return {
            'visualParityReport': report_data
        }
