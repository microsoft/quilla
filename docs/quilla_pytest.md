# Running Quilla tests with Pytest

Quilla is bundled with the `pytest-quilla` plugin, but it is disabled by default to prevent unexpected behaviour. To start using Quilla with Pytest, add the line `use-quilla = True` to the project's pytest configuration (i.e. pytest.ini, setup.cfg, etc). Setting this flag will allow any JSON file with a specific prefix (by default, files that match `quilla*.json`) to be discovered by Pytest as a Quilla test.

## Why Pytest?

There are many test frameworks available, even if limiting only to those that are available for Python. Pytest, however, offers some unique features that Quilla benefits greatly from, and in turn Quilla enhances the features of Pytest. These are discussed below.

### Automatic test discovery

Quilla was originally designed to execute a single file's tests, which simplified the execution logic and the CLI. Pytest's test discovery feature then makes it incredibly easy to extend Quilla to an arbitrary number of files without having to write a new test discovery functionality

### Fail-only Reporting

Quilla provides robust reporting for its tests, and will output the full report (and the test outputs) regardless of the test's success or failure status. This enables advanced users to chain multiple Quilla tests together using the various outputs that they produce. However, most users do not need this, and likely will not concern themselves with checking the output unless the tests have failed. Pytest's reporting tool will only show the output of a test when it fails, which covers most of the basic usecase

### Rich plugin support

It is incredibly easy to write a Pytest plugin, and the logic for the `pytest-quilla` plugin is kept completely separate from the `quilla` logic. This allows Quilla to distribute both packages easily, and lets the `pytest-quilla` plugin automatically inherit features from the `quilla` plugin without having to re-write any of the plugin code, provided that the basic interface it uses remains unchanged.

Pytest's rich plugin support also means Quilla can already leverage the community. A great example of this is using Quilla with the `pytest-xdist` plugin, which enables Quilla to leverage multi-processing without having to add in multiprocessing features to Quilla.

### Dynamic test suite creation

Using Pytest markers, Quilla can leverage existing functionality to make it easy for users to create entire test suites on the fly. By properly labelling their Quilla tests with custom markers, users can opt to only run some tests, and keeping track of which test suite a given test belongs to happens at the test-level, as opposed to traditional methods which require different inventory files to keep track of tests.

Read more about the use of custom markers on the [pytest documentation](https://docs.pytest.org/en/6.2.x/example/markers.html)

## Adding Quilla CLI options when running in Pytest

The `pytest-quilla` plugin adds a CLI option to Pytest, allowing it to pass those specified options to the Quilla contexts. To specify a definition file named 'Definitions.json', for example, run pytest with the following command: `pytest --quilla-opts="--definitions test/definitions/Definitions.json"`

## Changing Quilla test prefix

Setting the ini option `quilla-prefix` will allow custom prefix options. For example, to have pytest register all JSON files matching `test_*.json` as Quilla tests, set `quilla-prefix = test_` in the project's pytest configuration

## Using Pytest with uiconf.py plugins file

Plugins will still be discovered when running Quilla, and must be installed or placed in the same directory that the project's pytest configuration is in. Simply add a `uiconf.py` file in the same directory as the setup.cfg (or pytest.ini, tox.ini, etc), and Quilla will take care of the rest

## Adding test markers to Quilla tests

Quilla tests support static markers in the JSON files. Add a 'markers' key to the top level of the JSON document. Examples of this can be found within the `tests/integration` directory of the Quilla repository, since all these tests are marked with the `integration` and `slow` markers.

It is not however possible to add markers that require additional parameters at this time to individual quilla tests through the JSON document. For example, the `skipif` marker requires a boolean to determine whether the test should be skipped or not, and it is not possible to do so at this time. The `skip` marker, however, does indeed work: the `reason` field can be omitted.

## Quilla and pytest-xdist

The `pytest-xdist` plugin is fully compatible with Quilla! Quilla uses the `pytest-xdist` to parallelize the tests, since all integration tests are written as Quilla tests and each test has an isolated context. It is encouraged, given how browser tests are usually slow, to use `pytest-xdist` to speed up the testing suite.
