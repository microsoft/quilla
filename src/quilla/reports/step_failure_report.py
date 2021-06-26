from typing import Union

from quilla.common.enums import (
    UITestActions,
    ReportType,
)
from quilla.reports.base_report import BaseReport


class StepFailureReport(BaseReport):
    '''
    Data class for specifying the cause of a step failing in a critical, usually unexpected way.

    Args:
        exception: Either an actual exception class, or a string that describes the failure
        browser: The name of the browser this action failed on
        action: An enum describing the action that was taken
        step_index: The index of the step that failed, for debugging purposes

    Attributes:
        index: The index of the step that failed, for debugging purposes
    '''
    def __init__(
        self,
        exception: Union[Exception, str],
        browser: str,
        action: UITestActions,
        step_index: int
    ):
        super().__init__(ReportType.STEP_FAILURE, browser, action, repr(exception))
        self.index = step_index

    def to_dict(self):
        '''
        Converts this report into a dictionary object

        Returns:
            a dictionary containing the representation of this object
        '''
        return {
            'stepFailureReport': {
                'action': self.action.value,
                'targetBrowser': self.browser,
                'passed': False,
                'stepIndex': self.index,
                'msg': self.msg,
            }
        }

    @classmethod
    def from_dict(cls, report_dict):
        '''
        Converts a dictionary representing this object into a proper StepFailureReport object

        Returns:
            the appropriate StepFailureReport object
        '''
        report = report_dict['stepFailureReport']
        return StepFailureReport(
            report['msg'],
            report['targetBrowser'],
            cls._name_to_enum(report['action'], UITestActions),
            report['stepIndex']
        )
