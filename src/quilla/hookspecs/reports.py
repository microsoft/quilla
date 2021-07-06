'''
Hooks related to outputs and reports
'''

from quilla.ctx import Context
from quilla.hookspecs import hookspec
from quilla.reports.report_summary import ReportSummary


@hookspec
def quilla_postvalidate(ctx: Context, reports: ReportSummary):
    '''
    A hook called immediately after all validations are executed and the full
    ReportSummary is generated

    Args:
        ctx: The runtime context for the application
        reports: An object capturing all generated reports and giving summary data
    '''
