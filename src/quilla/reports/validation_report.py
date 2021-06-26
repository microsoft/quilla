from quilla.common.enums import (
    ReportType,
    UITestActions,
)
from quilla.reports.base_report import BaseReport


class ValidationReport(BaseReport):
    '''
    Data class for producing reports on the results of the validations

    Args:
        validation_type: The string representation of the type of validation performed
        target: The validation target
        state: The desired state used for validation
        browser_name: The name of the browser that the validation was performed on
        success: Whether the validation passed or not
        msg: An optional string adding further context to the report

    Attributes:
        validation_type: The string representation of the type of validation performed
        target: The validation target
        state: The desired state used for validation
        success: Whether the validation passed or not
        msg: An optional string adding further context to the report
    '''

    def __init__(
        self,
        validation_type: str,
        target: str,
        state: str,
        browser_name: str,
        success: bool,
        msg: str = ""
    ):
        super().__init__(
            ReportType.VALIDATION,
            browser_name,
            UITestActions.VALIDATE,
            msg
        )
        self.validation_type = validation_type
        self.target = target
        self.state = state
        self.success = success

    @classmethod
    def from_dict(cls, report) -> "ValidationReport":
        '''
        Converts a dictionary into a ValidationReport object

        Args:
            report:
        '''
        params = report['validationReport']
        msg = ""
        if 'msg' in params:
            msg = params['msg']
        return ValidationReport(
            validation_type=params['type'],
            target=params['target'],
            state=params['state'],
            browser_name=params['targetBrowser'],
            success=params['passed'],
            msg=msg
        )

    def to_dict(self):
        '''
        Returns a dictionary representation of the object
        '''
        report = {
            "validationReport": {
                "action": self.action.value,
                "type": self.validation_type,
                "target": self.target,
                "state": self.state,
                "targetBrowser": self.browser,
                "passed": self.success,
            }
        }

        if self.msg:
            report['validationReport']['msg'] = self.msg

        return report
