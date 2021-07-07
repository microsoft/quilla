# All of these variables can be set as env variables instead

DOCS_BUILD_DIR    ?= _build
DOC_TARGETS       ?= html man
PYTHON_EXECUTABLE ?= python3
DIST_DIR          ?= dist
CLEAN_CMDS        ?= clean-python clean-docs clean-build
SDIST_OPTS		  ?=
SDIST             ?= sdist --dist-dir $(DIST_DIR) $(SDIST_OPTS)
BDIST_OPTS        ?=
BDIST_WHEEL       ?= bdist_wheel --dist-dir $(DIST_DIR) $(BDIST_OPTS)
PACKAGE_TARGETS   ?= $(SDIST) $(BDIST_WHEEL)
PACKAGE_OPTS      ?=


.PHONY: help
help: ## Print this help message and exit
	@echo Usage:
	@echo "  make [target]"
	@echo
	@echo Targets:
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "  %-30s %s\n", $$1, $$NF \
		 }' $(MAKEFILE_LIST)

.PHONY: package
package:  ## Create release packages
	$(PYTHON_EXECUTABLE) setup.py $(PACKAGE_TARGETS) $(PACKAGE_OPTS)

.PHONY: package-deps
package-deps:  ## Create wheel files for all runtime dependencies
	$(PYTHON_EXECUTABLE) -m pip wheel --wheel-dir $(DIST_DIR) $(PACKAGE_OPTS) .

.PHONY: docs
docs: ## Build all the docs in the docs/_build directory
	$(MAKE) -C $@ $(DOC_TARGETS) BUILDDIR=$(DOCS_BUILD_DIR)

.PHONY: clean-python
clean-python:  ## Cleans all the python cache & egg files files
	$(RM) `find . -name "*.pyc" | tac`
	$(RM) -d `find . -name "__pycache__" | tac`
	$(RM) -r `find . -name "*.egg-info" | tac`

.PHONY: clean-docs
clean-docs:  ## Clean the docs build directory
	$(RM) -r docs/$(DOCS_BUILD_DIR)

.PHONY: clean-build
clean-build:  ## Cleans all code build and distribution directories
	$(RM) -r build $(DIST_DIR)

.PHONY: clean
clean:  ## Cleans all build, docs, and cache files
	$(MAKE) $(CLEAN_CMDS)

.PHONY: install
install:  ## Installs the package
	$(PYTHON_EXECUTABLE) -m pip install .

.PHONY: install-docs
install-docs:  ## Install the package and docs dependencies
	$(PYTHON_EXECUTABLE) -m pip install -e .[docs]

.PHONY: install-tests
install-tests:  ## Install the package and test dependencies
	$(PYTHON_EXECUTABLE) -m pip install -e .[tests]

.PHONY: install-all
install-all:  ## Install the package, docs, and test dependencies as well as pre-commit hooks
	$(PYTHON_EXECUTABLE) -m pip install -e .[all] && pre-commit install
