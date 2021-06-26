# Context Expressions

## Overview

Quilla enables test writers to dynamically create their tests using context expressions and context objects. This allows test writers to write validations that might require sensitive data that should not be committed to files (such as passwords for logging in), as well as reacting appropriately to potentially dynamic components of their applications. Beyond that, context expressions can be extended through plugins to incorporate more advanced behaviours such as retrieving secrets from a keystore.

Context expressions can be used whenever Quilla expects a non-enumerated value. This means that, while you can control the target of your `Click` action through a context expression, you cannot control the action itself through a context expression. This is because Quilla must be able to ensure at "compile time" (i.e. when the file is first loaded in to Quilla) that all the actions being performed are supported actions.

The syntax for context expressions is `${{ <CONTEXT_OBJECT_NAME>.<PATH_TO_VALUE> }}`. For the `Validation` and `Definitions` context objects, this is represented as a dot-separated path of a dictionary (i.e. to get the value `"ham"` from `{"spam": {"eggs": "ham"}}`, it would be accessed by `${{ Validation.spam.eggs }}`).

At this time, Quilla does not run `eval` on the context expression. This means that, while context expressions allow you to replace the values, you cannot write pure python code inside the context expression.

Below is a table that describes the included context objects.

| Context Object Name | Description | Example |
|:-------------------:|:-----------:|:-------:|
| Definitions | Resolves a name from the passed-in definition files or local definitions | `${{ Definitions.MyService.HomePage.SubmitButton }}` |
| Environment | Accesses environment variables, where `<PATH_TO_VALUE>` matches exactly the name of an environment variable | `${{ Environment.PATH }}` |
| Validation | Accesses previous outputs created by the validation | `${{ Validation.my.output }}` |

## Context Objects

### Definitions

The `Definitions` context object is a way to use an external file to hold any text data that is better stored with additional context. This is particularly useful for maintaining a definitions file for all XPaths used. Since most XPaths contain paths, IDs, and other element identifying information, they are not normally easy to understand at a glance. By using definitions files, each XPath used in a validation file can have a proper name associated with it, making validation files easier to read.

As an additional benefit, definition files allow test writers to quickly adapt to changes in how elements are identified on a page. If, for example, a developer changes the ID of a 'Submit' button, test writers can ensure that all tests that require the use of that submit button are using the new, correct identifier by changing it in just one place.

Below is an example definitions file:

```json
// Definitions.json
{
    "HomePage": {
        "SearchTextField": "//input[@id='search']",
        "SearchSubmitButton": "//button[@id='form_submit']"
    }
}
```

We can then use these directly inside of our validation

```json
// HomePageSearchTest.json
{
    "targetBrowsers": ["Edge"],
    "path": "https://example.com",
    "steps": [
        {
            "action": "SendKeys",
            "target": "${{ Definitions.HomePage.SearchTextField }}",
            "parameters": {
                "data": "puppies"
            }
        },
        {
            "action": "Click",
            "target": "${{ Definitions.HomePage.SearchSubmitButton }}"
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "puppies"
        }
    ]
}
```

When calling quilla, we pass in the definitions file: `quilla -d Definitions.json -f HomePageSearchTest.json`.

If we wanted there to be better legibility but not use the definitions anywhere else, we could also specify them inside the quilla test file itself. We see an example of that below:

```json
// HomePageSearchTest.json
{
    "definitions": {
        "HomePage": {
            "SearchTextField": "//input[@id='search']",
            "SearchSubmitButton": "//button[@id='form_submit']"
        }
    },
    "targetBrowsers": ["Edge"],
    "path": "https://example.com",
    "steps": [
        {
            "action": "SendKeys",
            "target": "${{ Definitions.HomePage.SearchTextField }}",
            "parameters": {
                "data": "puppies"
            }
        },
        {
            "action": "Click",
            "target": "${{ Definitions.HomePage.SearchSubmitButton }}"
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "puppies"
        }
    ]
}
```

Quilla will accept multiple definition files by adding multiple `-d <FILENAME>` groups to the CLI. It will attempt to resolve any duplicates by performing a deep merge operation between the multiple definition files, as well as any definitions specified in the quilla test file. The load order for the definition files is provided below:

1. First definition file specified to the CLI
1. Second definition file specified to the CLI
1. (...)
1. The last definition file specified to the CLI
1. Local definitions in the Quilla test file

If there are conflicts encountered, Quilla will favour the newer configs (i.e. second definition file overrides first, etc).

Quilla definitions can also be defined recursively. Quilla will attempt to evaluate the context expression iteratively until it has exhausted the context expressions in the string, so definitions do not have a limit to the recursive depth. This is useful when a definition is in part determined by other definitions, and reduces the amount of repetition in the Quilla files.

Below is an example definition file that uses recursive definitions:

```json
// Definitions.json
{
    "HomePage": {
        "HeaderSection": "//div[@id='header']",
        "SignInButton": "${{ Definitions.HomePage.HeaderSection }}/a[@id='login']"
    }
}
```

When calling `${{ Definitions.HomePage.SignInButton }}`, Quilla will expand it to `"//div[@id='header']/a[@id='login']"`.

### Environment

The `Environment` context object works as a pass-through to `os.environ.get(<PATH_TO_VALUE>, '')`. This means that Quilla will fail silently if the variable that you attempt to extract from the environment does not exist. Most likely, this will result in other failures of the ui validation. If you use this context object and are getting unexpected errors, check to make sure that the variable is set and that you have not made a typo on the variable name!

### Validation

The `Validation` context object will attempt to access a data store represented by a dictionary. This data store is populated at runtime through the `OutputValue` action, enabling any value that was created through the validations to be used inline.
