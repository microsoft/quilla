import json
from abc import (
    abstractclassmethod,
    abstractmethod,
)
from typing import Dict

from quilla.common.utils import EnumResolver
from quilla.common.enums import (
    ReportType,
    UITestActions,
)


class BaseReport(EnumResolver):
    '''
    Data class for producing reports on various steps performed

    Args:
        report_type: An enum specifying the kind of report
        browser: The name of the browser
        action: An enum specifying the kind of action that was taken
        msg: A string giving further context to the report
    '''

    def __init__(self, report_type: ReportType, browser: str, action: UITestActions, msg: str = ""):
        self.browser: str = browser
        self.action: UITestActions = action
        self.msg: str = msg
        self.report_type: ReportType = report_type

    @abstractclassmethod
    def from_dict(cls, report: Dict[str, Dict[str, str]]) -> "BaseReport":
        '''
        Converts a dictionary report into a valid Report object

        Args:
            report: a dictionary that describes a report
        '''

    @abstractmethod
    def to_dict(self):
        '''
        Converts the Report object into a dictionary representation
        '''

    def to_json(self) -> str:
        '''
        Returns:
            a json representation of the object. Good for passing reports to different applications
        '''
        report = self.to_dict()
        return json.dumps(report)

    @classmethod
    def from_json(cls, report_json: str) -> "BaseReport":
        '''
        Loads a valid json string and attempts to convert it into a Report object

        Returns:
            a report of the appropriate type
        '''
        st = json.loads(report_json)
        return cls.from_dict(st)  # type: ignore

    @classmethod
    def from_file(cls, fp) -> "BaseReport":
        '''
        Converts a fp (a file-like .read() supporting object) containing a json document
        into a Report object

        Returns:
            a report of the appropriate type
        '''
        st = json.load(fp)
        return cls.from_dict(st)  # type: ignore
