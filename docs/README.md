# Documentation

## Style

The Quilla module is extensively documented using the Google Docstring style (see [example](https://www.sphinx-doc.org/en/master/usage/extensions/example_google.html) here), and uses [Sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate the documentation.

## Dependencies

The following Python packages are used to create all the documentation for this project

| Package                   | Usage                                                                   |
|---------------------------|:-----------------------------------------------------------------------:|
|`Sphinx`                   | Generating docs                                                         |
|`sphinx-rtd-theme`         | HTML Doocumentation style theme                                         |
|`sphinx_autodoc_typehints` | Detecting type hints                                                    |
|`myst_parser`              | Integrating markdown docs used in the repo into generated documentation |
|`sphinx_argparse_cli`      | Documenting the CLI usage                                               |

&nbsp;

## Building the Docs

### Building from the package directory

The preferred method for building documentation is to use the `make` commands provided in the root package directory.

Using environment variables or the command-line, you can further customize these options. The following table describes the variables you can use to customize the documentation process.

| Variable Name | Use | Default Values |
|:-------------:|:---:|:--------:|
| `DOC_TARGETS` | A space-separated list of values specifying what targets to build | `html man`|
| `DOCS_BUILD_DIR` | A directory (relative to the `docs` directory) in which to build the `make` targets | `_build` |

For more information on customizing `make` targets, check out the [makefile vars](makefile_vars.md) documentation

### Building from the `docs/` directory

All of the above packages are available through `pip` and can be installed with `pip install sphinx sphinx-rtd-theme sphinx_autodoc_typehints myst_parser`. They are also specified in the `setup.py` file, and can therefore be installed with `pip install .[docs]`

To generate the docs, run `make help` to see what targets are available. In general, these are common targets:

- `make html`
- `make man`
- `make latex`
- `make latexpdf`

> Note: Even though the `latexpdf` target will produce a PDF document, you need the required `tex` packages installed to generate it, and those are not provided with sphinx. Installing `apt` packages such as `tex-common`, `texlive-full`, etc. may help, but installation of the specific packages is out of scope for this documentation and should be handled by the end user.
