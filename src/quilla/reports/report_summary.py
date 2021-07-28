import json
from typing import (
    Dict,
    Type,
    List,
    Callable
)

from quilla.common.enums import ReportType
from quilla.reports.base_report import BaseReport
from quilla.reports.validation_report import ValidationReport
from quilla.reports.step_failure_report import StepFailureReport
from quilla.reports.visual_parity_report import VisualParityReport


class ReportSummary:
    '''
    A class to describe a series of report objects, as well as manipulating them for test purposes.

    Args:
        run_id: A string that uniquely identifies the run
        outputs: The outputs generated by various steps
        reports: A list of reports to produce a summary of

    Attributes:
        run_id: A string that uniquely identifies the run
        outputs: The outputs generated by various steps
        reports: A list of reports used to produce a summary
        successes: The number of reports that are described as successful
        fails: The numer of reports that are not described as successful
        critical_failures: The number of reports representing critical (i.e. unrecoverable)
            failures. This will be produced at any step if it causes an exception.
        filter_by: A declarative way to filter through the various reports
    '''
    selector: Dict[str, Type[BaseReport]] = {
        'validationReport': ValidationReport,
        'stepFailureReport': StepFailureReport,
        'visualParityReport': VisualParityReport,
    }

    def __init__(self, run_id: str, outputs: dict, reports: List[BaseReport] = []):
        self.run_id = run_id
        self.outputs = outputs
        self.reports = reports
        self.successes = 0
        self.fails = 0
        self.critical_failures = 0
        self.filter_by = ReportSummary.FilterTypes(self)
        self._summarize()

    def to_dict(self):
        '''
        Returns:
            a dictionary representation of the summary report
        '''
        return {
            'reportSummary': {
                'total_reports': len(self.reports),
                'successes': self.successes,
                'failures': self.fails,
                'critical_failures': self.critical_failures,
                'reports': [
                    report.to_dict() for report in self.reports
                ]
            },
            'outputs': self.outputs,
            'run_id': self.run_id,
        }

    def to_json(self) -> str:
        '''
        Returns:
            a json string representation of the summary report
        '''
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, summary_dict: dict):
        '''
        Loads a ReportSummary object that is represented as a dictionary. It does not trust the
        metadata that is in the report, and will regenerate the metadata itself.
        '''
        reports = summary_dict['reportSummary']['reports']
        run_id = summary_dict.get('run_id', '')
        outputs = summary_dict.get('outputs', {})
        obj_reports = []
        for report in reports:
            # Each report has a report tag as the root of the json document
            report_type = list(report.keys())[0]
            report_object = cls.selector[report_type]
            obj_reports.append(report_object.from_dict(report))
        obj_reports = [ValidationReport.from_dict(report) for report in reports]
        return ReportSummary(run_id, outputs, obj_reports)

    @classmethod
    def from_json(cls, summary_json):
        '''
        Loads a ReportSummary object that is represented as a valid json string. Calls from_dict
        with the default json loader
        '''
        return cls.from_dict(json.loads(summary_json))

    def _summarize(self):
        '''
        Performs the summary operation over the stored reports
        '''
        for report in self.reports:
            if report.report_type == ReportType.VALIDATION:
                if report.success:
                    self.successes += 1
                else:
                    self.fails += 1
            elif report.report_type == ReportType.STEP_FAILURE:
                self.fails += 1
                self.critical_failures += 1

    class FilterTypes:
        '''
        Inner class used to provide declarative filtering syntax for ReportSummary objects.
        For example, to filter by only successful reports you would call
        `reports.filter_by.success()`
        '''
        def __init__(self, summary: 'ReportSummary'):
            self._summary = summary
            self._run_id = summary.run_id

        def _filter(self, condition: Callable[[BaseReport], bool]) -> 'ReportSummary':
            '''
            Returns a new summary with only reports that match the condition passed as
            a lambda function parameter
            '''
            reports = self._summary.reports.copy()
            filtered_reports = filter(condition, reports)

            return ReportSummary(self._run_id, {}, list(filtered_reports))

        def state(self, state: str) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only reports that have a state matching the one
                given by the state parameter
            '''
            return self._filter(
                lambda x: isinstance(x, ValidationReport) and x.state.lower() == state
            )

        def browser(self, browser: str) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only reports that have a browser matching the one
                given by the browser parameter
            '''
            return self._filter(lambda x: x.browser.lower() == browser.lower())

        def successful(self) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only the reports that produced a success
            '''
            return self._filter(lambda x: isinstance(x, ValidationReport) and x.success)

        def failure(self) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only the reports that produced a failure
            '''
            return self._filter(lambda x: isinstance(x, ValidationReport) and not x.success)

        def type(self, validation_type: str) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only reports that have a type matching the one
                given by the type parameter
            '''
            return self._filter(
                lambda x:
                    isinstance(x, ValidationReport) and
                    x.validation_type.lower() == validation_type.lower()
            )

        def target(self, target: str) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only reports that have a target matching the one
                given by the target parameter
            '''
            return self._filter(
                lambda x: isinstance(x, ValidationReport) and x.target.lower() == target.lower()
            )

        def critical_failure(self) -> 'ReportSummary':
            '''
            Returns:
                a new summary with only reports that constitute a critical failure
            '''

            return self._filter(lambda x: x.report_type == ReportType.STEP_FAILURE)