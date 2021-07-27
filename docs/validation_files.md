# Validation Files

Quilla operates through validation files, which are `JSON` files that define the environment and process for performing a validation in a declarative way. Each validation file requires the following:

- One or more target browsers (Firefox, Chrome, Edge)
- A starting URL path
- A list of steps

Each step can be either a setup step, or a validation step. Setup steps do not ordinarily provide any reports if they are successful, and Quilla will abort the test if any steps cause an error, as it will assume that the error is not recoverable. In this case, a `StepFailureReport` will be produced, and the `ReportSummary` will indicate that there is a critical failure.

Validation steps will produce a `ValidationReport`, which can result in either a success or a failure. Although the hope is that every test you write will result in a success, Quilla will not abort if a validation fails, and will continue the test until it is finished or otherwise aborted. However, if in attempting to perform the validation some unrecoverable error occurs, Quilla will instead produce a `StepFailureReport` with the exception that occurred and abort the execution.

All Quilla integration tests are written as quilla tests and therefore can be referenced as examples when writing new Quilla tests.

## Supported actions

The table below summarizes all the supported actions, what they do, and what they require. The `Validate` and `OutputValue` actions are omitted from this table and are shown in later sections.

| Action | Description | Target | Parameters |
|--------|-------------|--------|------------|
| `Refresh` | Refreshes the current page | None | None |
| `NavigateBack` | Navigates back to the last page | None | None |
| `NavigateForward` | Navigates forward to the next page | None | None |
| `NavigateTo` | Navigates to the target URL | `URL` | None |
| `Click` | Clicks an element on the page | `XPath` | None |
| `Clear` | Clears the text from an element on the page | `XPath` | None |
| `Hover` | Hovers the cursor over the target element on the page | `XPath` | None |
| `SendKeys` | Types the specified keys onto the target element on the page | `XPath` |  `data` |
| `WaitForExistence` | Waits until a target element exists on the page | `XPath` | `timeoutInSeconds` |
| `WaitForVisibility` | Waits until a target element is visible on the page | `XPath` | `timeoutInSeconds` |
| `SetBrowserSize` | Sets the browser size to a specific width & height | None | `width`, `height` |

## Output Values

Quilla is able to create 'outputs', which allows users to use values from the page within their own validations. This can come in handy when you need to react to the data on the page. A classic example is an application that displays some text that it requires the user to then type into a text field: instead of hardcoding the value for the UI tests (which may be impossible if the values are dynamically generated), a Quilla test could instead read the value from the XPath and use it in the same validation.

Below is a table displaying the supported output sources, the targets they support, and the parameters they require. Every single output requires an `outputName` parameter.

| Source | Description | Target type | Parameters |
|--------|-------------|-------------|------------|
| `Literal` | Creates an output from the literal value of the target | `string` | None |
| `XPathText` | Creates an output from the inner text value of the target | `XPath` | None |
| `XPathProperty` | Creates an output from the value of the specified property name of the target | `XPath` | `parameterName` |

## Validations

Each validation is performed when the `"action"` is set to `Validate`. The kind of validation is provided by the `"type"` key, and by default Quilla currently supports the `URL` and `XPath` types.

Each validation type supports a series of states provided by the `"state"` key, and requires some form of target to specify what is being validated.

### XPath Validation

Each `XPath` validation requires a `"target"` key with an `XPath` that describes an element on the page. The state of this `XPath` will then be validated, according to the valid states.

Some `XPath` validations also require parameters, such as the Attribute and Parameter-based validations of web elements.

The table below describes what the supported states are, and what they are validating

| State | Description | Parameters |
|-------|-------------|------------|
| `Exists` | The specified target exists on the page | None |
| `NotExists` | The specified target does *not* exist on the page | None |
| `Visible` | The specified target is visible on the page | None |
| `NotVisible` | The specified target is not visible on the page | None |
| `TextMatches` | Validates that the element text matches a regular expression pattern | `pattern` |
| `NotTextMatches` | Validates that the element text does not match a regular expression pattern | `pattern` |
| `HasProperty` | Ensures that the element has a property with a matching name | `name` |
| `NotHasProperty` | Ensures that the element does not have a property with a matching name | `name` |
| `HasAttribute` | Ensures that the element has an attribute with a matching name | `name` |
| `NotHasAttribute` | Ensures that the element does not have an attribute with a matching name | `name` |
| `PropertyHasValue` | Ensures that the property has a value matching the one specified | `name`, `value` |
| `NotPropertyHasValue` | Ensures that the property does not have a value matching the one specified | `name`, `value` |
| `AttributeHasValue` | Ensures that the attribute has a value matching the one specified | `name`, `value` |
| `AttributeHasValue` | Ensures that the attribute does not have a value matching the one specified | `name`, `value` |
| `VisualParity` | Checks previous baseline images pixel-by-pixel to ensure that sections have not changed | `baselineID` |

> Note: The `VisualParity` state is discussed more at length in the [visual parity](visual_parity.md) section. For information on how to write storage plugins for `VisualParity` to use, check out the "Storage Plugins" section of the [plugins](plugins.md) docs.

### URL Validation

Each `URL` validation requires a `"target"` key with a string. The precise target will be defined by the `"state"` property.

| State | Description |
|-------|-------------|
| `Equals` | The specified target is exactly equal to the URL of the page at the time the validation runs |
| `NotEquals` | The specified target is not equal to the URL of the page at the time the validation runs |
| `Contains` | The specified target is a substring of the URL of the page at the time the validation runs |
| `NotContains` | The specified target is not a substring of the URL of the page at the time the validation runs |

## Examples

### Searching Bing for puppies

Example written in 2021-06-16

```json
{
    "definitions": {
        "HomePage": {
            "SearchTextBox": "//input[@id='sb_form_q']",
            "SearchButton": "//label[@for='sb_form_go']",
        },
        "ResultsPage": {
            "MainInfoCard": "//div[@class='lite-entcard-main']"
        }
    },
    "targetBrowsers": ["Firefox"],
    "path": "https://www.bing.com",
    "steps": [
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "bing"
        },
        {
            "action": "Validate",
            "type": "XPath",
            "state": "Exists",
            "target": "${{ Definitions.HomePage.SearchTextBox }}"
        },
        {
            "action": "Validate",
            "type": "XPath",
            "state": "Exists",
            "target": "${{ Definitions.HomePage.SearchButton }}"
        },
        {
            "action": "SendKeys",
            "target": "${{ Definitions.HomePage.SearchTextBox }}",
            "parameters": {
                "data": "Puppies"
            }
        },
        {
            "action": "Click",
            "target": "${{ Definitions.HomePage.SearchButton }}"
        },
        {
            "action": "WaitForExistence",
            "target": "${{ Definitions.ResultsPage.MainInfoCard }}",
            "parameters": {
                "timeoutInSeconds": 10
            }
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "search?q=Puppies"
        }
    ]
}
```

### Signing In to Github

Example written on 2021-06-24

```json
{
    "definitions": {
        "Username": "${{ Environment.GITHUB_EXAMPLE_USER_USERNAME }}",
        "Password": "${{ Environment.GITHUB_EXAMPLE_USER_PASSWORD }}",
        "WelcomePage": {
            "SignInButton": "//div[@class='position-relative mr-3']/a"
        },
        "SignInPage": {
            "UsernameInputField": "//input[@id='login_field']",
            "PasswordInputField": "//input[@id='password']",
            "SubmitButton": "//input[@class='btn btn-primary btn-block']"
        },
        "HomePage": {
            "UserMenuIcon": "//div[@class='Header-item position-relative mr-0 d-none d-md-flex']",
            "YourProfileDropdown": "//details-menu/a[@href='/${{ Definitions.Username }}']"
        }
    },
    "targetBrowsers": ["Firefox"],
    "path": "https://github.com",
    "steps": [
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "github"
        },
        {
            "action": "Validate",
            "type": "XPath",
            "state": "Exists",
            "target": "${{ Definitions.WelcomePage.SignInButton }}"
        },
        {
            "action": "Validate",
            "type": "XPath",
            "target": "${{ Definitions.WelcomePage.SignInButton }}",
            "state": "TextMatches",
            "parameters": {
                "pattern": "[Ss]ign[ -]?[Ii]n"
            }
        },
        {
            "action": "Click",
            "target": "${{ Definitions.WelcomePage.SignInButton }}"
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "/login"
        },
        {
            "action": "Clear",
            "target": "${{ Definitions.SignInPage.UsernameInputField }}"
        },
        {
            "action": "Clear",
            "target": "${{ Definitions.SignInPage.PasswordInputField }}"
        },
        {
            "action": "SendKeys",
            "target":"${{ Definitions.SignInPage.UsernameInputField }}",
            "parameters": {
                "data": "${{ Definitions.Username }}"
            }
        },
        {
            "action": "SendKeys",
            "target": "${{ Definitions.SignInPage.PasswordInputField }}",
            "parameters": {
                "data": "${{ Definitions.Password }}"
            }
        },
        {
            "action": "Validate",
            "type": "XPath",
            "target": "${{ Definitions.SignInPage.PasswordInputField }}",
            "state": "HasAttribute",
            "parameters": {
                "name": "id"
            }
        },
        {
            "action": "Validate",
            "type": "XPath",
            "target": "${{ Definitions.SignInPage.PasswordInputField }}",
            "state": "AttributeHasValue",
            "parameters": {
                "name": "id",
                "value": "password"
            }
        },
        {
            "action": "Click",
            "target": "${{ Definitions.SignInPage.SubmitButton }}"
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Equals",
            "target": "https://github.com/"
        },
        {
            "action": "Click",
            "target": "${{ Definitions.HomePage.UserMenuIcon }}"
        },
        {
            "action": "Click",
            "target": "${{ Definitions.HomePage.YourProfileDropdown }}"
        },
        {
            "action": "Validate",
            "type": "URL",
            "state": "Contains",
            "target": "${{ Definitions.Username }}"
        }
    ]
}
```
