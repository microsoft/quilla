# How does Quilla work?

Quilla is a wrapper on Selenium to allow for test writers to create their testing scenarios focusing not on how Selenium works, but on how their tests are executed. As such, the goal was to create a testing syntax that focuses on legibility, and uses minimal required setup. For further information on the specifics of how Quilla translates the JSON test files into workable code and runs the validations, read on.

## Code execution flow

When Quilla is called, it will first create and initialize the plugin manager. This is done by first loading all the plugins that are exposed through python entrypoints, then attempting to discover a `uiconf.py` file in the plugin root directory (which is at this time just the calling directory).

Next, Quilla will create the parser and pass it to the `quilla_addopts` hook to allow plugins to register new parser options. If the user has specified that they are passing in a filename, the file will then be read and the contents of the file will be saved as a string. It will then parse the CLI options and use them to create the default context.

The context object is initialized as follows:

1. A snapshot of the `PATH` variable is taken
1. The debug configurations are set
1. The driver path is added to the system `PATH` environment variable
1. The definition files will be loaded and merged

Once the context is initialized, it will be passed to the `quilla_configure` hook to allow plugins to alter the context.

When the configuration is finalized, the contents of the file will be loaded with the default JSON loader from python into a dictionary. This dictionary will then be processed as follows:

1. If the quilla test file has a 'definitions' key, it will be loaded and merged with the existing definitions
1. All specified browser names will be resolved into a `BrowserTargets` enum.
1. Each step will be processed as such:
    1. The action name for the step will be resolved into a `UITestActions` enum
    1. If the action is a `Validate` action, the type will be resolved into a `ValidationTypes` enum
        1. Based on the `ValidationTypes`, the appropriate `ValidationStates` subclass will be selected and the state will be resolved
    1. If there are parameters specified, they will be checked:
        1. If the "source" parameter is specified, it will be resolved into a `OutputSources` enum
1. The `UIValidation` object is then created with the fully-resolved dictionary
    1. A `StepsAggregator` instance is created to manage the creation of all proper step objects
        1. Each step in the list of step dictionaries will be resolved into the appropriate type, either a `TestStep` or something that can be resolved by the `Validation` factory class
    1. For each browser specified in the JSON file, a copy of the `StepsAggregator` object will be created and passed into a new `BrowserValidation` object

After the `UIValidation` object is created, it is passed to the `quilla_prevalidate` plugin hook. This hook is able to mutate the object however it sees fit, allowing end-users to manipulate steps dynamically.

When the `UIValidation` object is finalized, it will then call `validate_all()` to execute all browser validations sequentially. The order in which the browsers will be validated is the same order in which they were specified. When calling the `validate_all` function, the following will occur for each browser target:

1. An appropriate driver will be created and configured according to the runtime context, opening up a blank page
1. The driver will navigate to the root path of the validation
1. The `BrowserValidation` object will bind the current driver to itself, to each of its steps (through the `StepsAggregator`), and to the runtime context
1. Each step will be executed in order, performing the following:
    1. The action function is selected. For a `TestStep`, it is resolved based on the action associated to its `UITestActions` value through a dictionary selector. For a `Validation`, this is determined based on the `ValidationStates` subclass value (i.e. the `XPathValidationStates`, etc)
    1. If the action produces a report, add it to the list of resulting reports
    1. If the action produces an exception, a `StepFailureReport` will be generated and the rest of the steps will *not* be executed. This is substantially different from the `Validation` behaviour: the `Validate` action only describes the state of the page, so it does not necessarily mean that the steps following it are not able to be performed. Since almost every other action actually causes the state of the page to change, allowing the test to continue would mean allowing the execution of the next steps in an inconsistent state.
1. Once all steps have been executed, or an uncaught exception happens on the `StepsAggregator` (which will happen if the `suppress_exceptions` flag is set to `False` in the context object), the `BrowserValidation` will close the browser window, unbind the driver from itself, the steps, and the context.
1. If no exception was raised, the list of report objects will be returned

After each browser finishes executing, the returned reports are all aggregated and put into a `ReportSummary`, which is ultimately returned.

Once the final `ReportSummary` has been generated, it is passed (along with the runtime context) to the `quilla_postvalidate` hook.

Finally, the entire `ReportSummary` is converted into JSON alongside any outputs created by the test actions, which are then printed to the standard output. If the `ReportSummary` contains any failures, or critical failures, it will then return the exit code of 1, otherwise it will return an exit code of 0.
