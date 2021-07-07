import json

import pytest
from py._path.local import LocalPath

from quilla import (
    setup_context,
    execute
)
from quilla.reports.report_summary import ReportSummary


def collect_file(parent: pytest.Session, path: LocalPath, prefix: str):
    '''
    Collects files if their path ends with .json and starts with the prefix

    Args:
        parent: The session object performing the collection
        path: The path to the file that might be collected
        prefix: The prefix for files that should be collected

    Returns:
        A quilla file object if the path matches, None otherwise

    '''
    # TODO: change "path" to be "fspath" when pytest 6.3 is released:
    # https://docs.pytest.org/en/latest/_modules/_pytest/hookspec.html#pytest_collect_file
    if path.ext == ".json" and path.basename.startswith(prefix):
        return QuillaFile.from_parent(parent, fspath=path)


class QuillaFile(pytest.File):
    def collect(self):
        '''
        Loads the JSON test data from the path and creates the test instance

        Yields:
            A quilla item configured from the JSON data
        '''
        test_data = self.fspath.open().read()
        yield QuillaItem.from_parent(self, name=self.fspath.purebasename, test_data=test_data)


class QuillaItem(pytest.Item):
    def __init__(self, name: str, parent: QuillaFile, test_data: str):
        super(QuillaItem, self).__init__(name, parent)
        self.test_data = test_data
        json_data = json.loads(test_data)
        markers = json_data.get('markers', [])
        for marker in markers:
            self.add_marker(marker)

    def runtest(self):
        '''
        Runs the quilla test by creating an isolated context and executing the test
        data retrieved from the JSON file.
        '''
        ctx = setup_context(
            [*self.config.getoption('--quilla-opts').split(), ''],
            str(self.config.rootpath)
        )
        ctx.json = self.test_data
        results = execute(ctx)
        self.results = results
        try:
            assert results.fails == 0
            assert results.critical_failures == 0
        except AssertionError:
            raise QuillaJsonException(results)

    def repr_failure(self, excinfo):
        """Called when self.runtest() raises an exception."""
        if isinstance(excinfo.value, QuillaJsonException):
            results: ReportSummary = excinfo.value.args[0]
            return json.dumps(
                results.to_dict(),
                indent=4,
                sort_keys=True
            )
        super().repr_failure(excinfo=excinfo)

    def reportinfo(self):
        return self.fspath, 0, 'failed test: %s' % self.name


class QuillaJsonException(Exception):
    '''
    Custom exception for when Quilla files fail
    '''
