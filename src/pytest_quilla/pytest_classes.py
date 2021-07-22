import json

import pytest
from py._path.local import LocalPath

from quilla import (
    setup_context,
    execute
)
from quilla.reports.report_summary import ReportSummary


def collect_file(parent: pytest.Session, path: LocalPath, prefix: str, run_id: str):
    '''
    Collects files if their path ends with .json and starts with the prefix

    Args:
        parent: The session object performing the collection
        path: The path to the file that might be collected
        prefix: The prefix for files that should be collected
        run_id: The run ID of the quilla tests

    Returns:
        A quilla file object if the path matches, None otherwise

    '''
    # TODO: change "path" to be "fspath" when pytest 6.3 is released:
    # https://docs.pytest.org/en/latest/_modules/_pytest/hookspec.html#pytest_collect_file
    if path.ext == '.json' and path.basename.startswith(prefix):
        return QuillaFile.from_parent(parent, fspath=path, run_id=run_id)


class QuillaFile(pytest.File):
    def __init__(self, *args, run_id: str = '', **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.quilla_run_id = run_id

    def collect(self):
        '''
        Loads the JSON test data from the path and creates the test instance

        Yields:
            A quilla item configured from the JSON data
        '''
        test_data = self.fspath.open().read()
        yield QuillaItem.from_parent(
            self,
            name=self.fspath.purebasename,
            test_data=test_data,
            run_id=self.quilla_run_id
        )


class QuillaItem(pytest.Item):
    def __init__(self, name: str, parent: QuillaFile, test_data: str, run_id: str):
        super(QuillaItem, self).__init__(name, parent)
        self.test_data = test_data
        self.quilla_run_id = run_id
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
            [*self.config.getoption('--quilla-opts').split()],
            str(self.config.rootpath),
            recreate_context=True
        )
        ctx.logger.debug('Quilla options discovered: %s', self.config.getoption('--quilla-opts'))
        if not (
            '-i' in self.config.getoption('--quilla-opts') or
            '--run-id' in self.config.getoption('--quilla-opts')
        ):
            ctx.run_id = self.quilla_run_id

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
