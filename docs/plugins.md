# Plugins

The Quilla framework supports the use of both installed and local plugins. This is done to allow for
maximum extensibility, while still only allowing for controlled access.

## Why Plugins

First and foremost, plugins allow the community to extend the behaviours of Quilla as well as for
individual users to be able to have more granular configuration control over the module.

Secondly, plugins allow for individual users of this project to decouple platform- and use-specific logic
from the codebase of the entire project. For example, a user could use a specific secret store that
they would like to retrieve data from and inject into their validations dynamically. Instead of having
to find a way of doing so externally, they could write a plugin to add a 'Secrets' context object, connecting
their own code to the right secret store without having to expose it.

More examples of what can be done with plugins are found in the sections below.

## Plugin discovery

Quilla discovers the plugins by searching the installed modules for 'QuillaPlugins' entrypoints,
and by searching a local file (specifically, the `uiconf.py` file in the calling directory). The discovery
process is done by searching for the predefined hook functions (as found in the `hookspec` module). If
your module, or your `uiconf.py` file, provide a function with a hook name it will be automatically loaded
and used at the appropriate times. See the `hookspec` documentation to see exactly which plugins are currently
supported.

## Local Plugin Example - Configuration

Consider the example of a programmer that does not want to enable all of the debugging configurations, but does not
want the browser to run in headless mode. Without plugins, they would have to download the repository, make
changes to the code, install it, make changes to the code, and then run.

This is far too cumbersome for such a small change, but with plugins we can do it in just two lines!

1. In the directory that includes your validations, add a `uiconf.py` file
2. Add the following lines to `uiconf.py`:

```python
def quilla_configure(ctx):
    ctx.run_headless = False
```

And you are all done! No further steps are required, you can just run the `quilla` CLI from that directory
and the configurations will be seamlessly picked up.

## Local Plugin Example - Adding CLI Arguments

Using the plugin system one can also seamlessly add (and act on) different CLI arguments which can be used later
on by your plugin, or maybe even by someone else's plugin!

As an example, consider the example from above of the programmer that wants to run the browser outside of headless
mode. Perhaps they wish to keep the default behaviour as running without headless mode, but they don't want to change
code whenever they swap between modes. They would need to add a new CLI argument, and consume it for their configuration!

1. In the validations directory, add a `uiconf.py` file
2. Add the following lines to `uiconf.py`:

```python
def quilla_addopts(parser):
    parser.add_argument(
        '-H',
        '--headless',
        action='store_true',
        help='Run the browsers in headless mode'
    )

def quilla_configure(ctx, args):
    ctx.run_headless = args.headless
```

Now, whenever they run `quilla` it will run with the browsers not in headless mode,
if they run `quilla --headless` it will run with the browsers in headless mode, and if they run
`quilla --help`, they should see their CLI argument:

```text
usage: quilla [-h] [-f] [-d] [--driver-dir DRIVERS_PATH] [-P] [-H] json

Program to provide a report of UI validations given a json representation of the validations or given the filename
containing a json document describing the validations

positional arguments:
  json                  The json file name or raw json string

optional arguments:
  -h, --help            show this help message and exit
  -f, --file            Whether to treat the argument as raw json or as a file
  -d, --debug           Enable debug mode
  --driver-dir DRIVERS_PATH
                        The directory where browser drivers are stored
  -P, --pretty          Set this flag to have the output be pretty-printed
  -H, --headless        Run the browsers in headless mode
```

## Installed Plugin Example - Packaging

As a final example with our previous programmer, suppose they now want to publish this new package
to be used by others. They set up their package as follows:

```text
quilla-headless
+-- headless
|   +-- __init__.py
|   +-- cli_configs.py
+-- setup.py
```

```python
# Inside headless/cli_configs.py

def quilla_addopts(parser):
    parser.add_argument(
        '-H',
        '--headless',
        action='store_true',
        help='Run the browsers in headless mode'
    )

def quilla_configure(ctx, args):
    ctx.run_headless = args.headless
```

```python
# Inside setup.py

from setuptools import setup, find_packages

setup(
    name='quilla-headless',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'QuillaPlugins': ['quilla-headless = headless.cli_configs']
    }
)
```

And they run `pip install .` in the `quilla-headless` directory. Their new CLI option and plugin will
now be globally available to the programmer, no matter where they call it from. Anyone who installs their package
will also be able to use this new CLI option!

## Local Plugin Example - Context expressions

The Quilla framework includes the ability to use the `Validation` and `Environment` context objects
(discussed in the [context expression documentation](context_expressions.md)) out-of-the-box, which allows
validations to produce (and use) outputs, and use environment variables. However, it is also possible to add new context
objects through the use of plugins. In this example, we'll be creating a local plugin that will add the `Driver` context
object, which will give us some basic information on the state of the current driver.

1. Create a `uiconf.py` file in the directory
2. Add the following to the `uiconf.py` file:

    ```python
    def quilla_context_obj(ctx, root, path):
        # We only handle 'Driver' context objects, so return None
        # to allow other plugins to handle the object
        if root != 'Driver':
            return

        # We only support 'name' and 'title' so any path of length
        # longer than one cannot resolve with this plugin, but another
        # plugin could support it so we'll still return None here
        if len(path) > 1:
            return

        # Now we handle the actual options that we support
        opt = path[0]
        if opt == 'name':
            return ctx.driver.name
        if opt == 'title':
            return ctx.driver.title
    ```

3. Create the `Validation.json` file in the same directory
4. Add the following to the `Validation.json` file:

    ```json
    {
        "targetBrowsers": ["Firefox"],
        "path": "https://bing.ca",
        "steps": [
            {
                "action": "OutputValue",
                "target": "${{ Driver.name }}",
                "parameters": {
                    "source": "Literal",
                    "outputName": "browserName"
                }
            },
            {
                "action": "OutputValue",
                "target": "${{ Driver.title }}",
                "parameters": {
                    "source": "Literal",
                    "outputName": "siteTitle"
                }
            }
        ]
    }
    ```

5. Run `quilla -f Validation.json --pretty`. You should receive the following output:

    ```json
    {
        "Outputs": {
            "browserName": "firefox",
            "siteTitle": "Bing"
        },
        "reportSummary": {
            "critical_failures": 0,
            "failures": 0,
            "reports": [],
            "successes": 0,
            "total_reports": 0
        }
    }
    ```
