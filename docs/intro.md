<!--
THIS FILE CONTAINS THE INTRO CONTENTS
FROM THE `quilla/README.md` FILE SO IT WILL
BE DISPLAYED IN THE GENERATED DOCUMENTATION.
DO NOT EDIT THIS DIRECTLY, AND IF YOU EDIT
THE README FILE'S INTRO, MAKE SURE YOU COPY+PASTE
IT TO THIS FILE.

MAKE SURE ANY LOCAL LNKS IN THIS PAGE USE THE CORRECT
LOCATION
-->

# Quilla

## Declarative UI Testing with JSON

Quilla is a framework that allows test-writers to perform UI testing using declarative syntax through JSON files. This enables test writers, owners, and maintainers to focus not on how to use code libraries, but on what steps a user would have to take to perform the actions being tested. In turn, this allows for more agile test writing and easier-to-understand test cases.

Quilla was built to be run in CI/CD, in containers, and locally. It also comes with an optional integration with [pytest](https://pytest.org), so you can write your Quilla test cases as part of your regular testing environment for python-based projects. Check out the [quilla-pytest](quilla_pytest.md) docs for more information on how to configure `pytest` to auto-discover Quilla files, adding markers, and more.
