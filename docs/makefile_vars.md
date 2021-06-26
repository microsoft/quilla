# Makefile Variables

The following are all the makefile variables used

| Variable Name | Use | Defaults |
|---------------|-----|----------|
| `PYTHON_EXECUTABLE` | The python version to use for any targets that use python commands. If you are using virtual environments, this will auto-detect it, and only should be set if you have a specific need to change the executable used for the make commands | `python3` |
| `CLEAN_CMDS` | The `make` targets to be executed when running `make clean` | `clean-python clean-docs clean-build` |
| `DOC_TARGETS` | The `make` targets to build docs for. For more info on possible targets, run `make help` in the `quilla/docs` directory | `html man` |
| `DOCS_BUILD_DIR` | The directory to output the docs artifacts in. This will output in `quilla/docs/$(DOCS_BUILD_DIR)` | `_build`
| `DIST_DIR` | The directory in which distribution artifacts (`.whl` files, source distributions, etc) will be output to | `dist` |
| `SDIST` | The configurations for the source distribution target | `sdist --dist-dir $(DIST_DIR) $(SDIST_OPTS)` |
| `SDIST_OPTS` | Additional options for `SDIST` | |
| `BDIST_WHEEL` | The configurations for the wheel binary distribution target | `bdist_wheel --dist-dir $(DIST_DIR) $(BDIST_OPTS)` |
| `BDIST_OPTS` | Additional options for `BDIST_WHEEL` | |
| `PACKAGE_TARGETS` | The distribution targets for the `make package` command | `$(SDIST) $(BDIST_WHEEL)` |
| `PACKAGE_OPTS` | Additional options for the `make package` and `make package-deps` targets | |

## Examples

### Changing the distribution directory

```bash
    # Using options
    $ make package DIST_DIR="_dist"
```

```bash
    # Using environment variables
    $ DIST_DIR="_dist" make package
```

### Only build wheel packages

```bash
    # Using environment variables
    $ SDIST="" make package
```

```bash
    # Using options
    $ make package SDIST=""
```

### Build html, man, latexpdf, and epub docs targets

```bash
    # Using environment variables
    $ DOC_TARGETS="html man latexpdf epub" make docs
```
