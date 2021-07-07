# Preface

This document has been written to be used by a multitude of individuals who interact with Quilla: Test writers, web developers, plugin creators, and code maintainers. As such, not every part of this document is important to every user.

For all who are unfamiliar with the concept of XPaths, make sure to brush up on what they are. The W3C Schools website has a good section on them [here](https://www.w3schools.com/XML/xml_xpath.asp)

Test writers looking for basic information on how to write a test should start by reading the section on [writing validation files](validation_files.md). This covers the basics of how to write Quilla tests, including a couple of examples. Then, to extend tests using non-static information (such as getting data from the environment variables or from a definition file), test writers should read the section on [context expressions and context objects](context_expressions.md). If more extensible configuration or custom data sources (i.e. accessing a secret store) is needed, the section on [writing plugins](plugins.md) covers examples on how to write local plugins. For testing teams who are seeking to integrate Quilla tests with Pytest, the section on [the pytest-quilla integration](quilla_pytest.md) will cover how to enable running Quilla as part of pytest.

Web developer looking to maintain a definition file (or multiple definition files) for a QA team to write tests with should read the section on [context expressions and context objects](context_expressions.md), specifically the subsection on the `Definitions` context object.

Plugin creator, should be familiar with [context expressions and context objects](context_expressions.md) first, since they are a key aspect of exposing new functionality for test writers. Then, the material covered in the section on [how to write plugins](plugins.md) explains how plugins work in Quilla and how to publish one so that Quilla will auto-detect it. For quick reference, the [hooks](hooks.rst) section is available for an overview on available hooks, when they are called, and what data is exposed.

Code maintainer or those looking to make a contribution to the code, should first have a good understanding of [how quilla works](how_it_works.md), how to [write validation files](validation_files.md) and how to [use context objects](context_expressions.md) to understand the general structure of the data that Quilla processes. In addition, the section on [how plugins work](plugins.md) and [which plugin hooks are exposed](hooks.rst) will cover necessary plugin-related information.

For ease of maintenance, the [documentation section](README.md) covers what dependencies are used to build the documentation, how to build the documentation, and the documentation style. Finally, the [makefile variable documentatio](makefile_vars.md) has additional information on how to customize the make commands using various environment variables.
