# Quilla Step Cookbook

To make it easier to use Quilla, included below is a "cookbook" that showcases examples for every step definition that Quilla contains.

## Refreshing the page

```json
{
  "action": "Refresh"
}
```

## Navigate Back to the Last Page

```json
{
  "action": "NavigateBack"
}
```

## Navigate Forward to the Next Page

```json
{
  "action": "NavigateForward"
}
```

## Navigate to a Page Given Its URL

```json
{
  "action": "NavigateTo",
  "target": "https://bing.com"
}
```

## Clicking on a Page Element

```json
{
  "action": "Click",
  "target": "${{ Definitions.SubmitButton }}"
}
```

## Clearing an Input Box

```json
{
  "action": "Clear",
  "target": "${{ Definitions.UsernameInputBox }}"
}
```

## Hovering Over an Element

```json
{
  "action": "Hover",
  "target": "${{ Definitions.InfoIcon }}"
}
```

## Writing Text Into an Input

### Using Static Data

```json
{
  "action": "SendKeys",
  "target": "${{ Definitions.UsernameField }}",
  "parameters": {
    "data": "test_user1"
  }
}
```

### Using Environment Data

```json
{
  "action": "SendKeys",
  "target": "${{ Definitions.PasswordField }}",
  "parameters": {
    "data": "${{ Environment.TEST_USER_PASSWORD }}"
  }
}
```

## Waiting

### Wait for an Element to Exist

Waiting for at most 5 seconds

```json
{
  "action": "WaitForExistence",
  "target": "${{ Definitions.SubmitButton }}",
  "parameters": {
    "timeoutInSeconds": 5
  }
}
```

### Wait for an Element to be Visible

Waiting for at most 5 seconds

```json
{
  "action": "WaitForVisibility",
  "target": "${{ Definitions.HeaderBannerImage }}",
  "parameter": {
    "timeoutInSeconds": 5
  }
}
```

## Setting Browser Size

Setting the window to be 800px by 600px

```json
{
  "action": "SetBrowserSize",
  "parameters": {
    "width": 800,
    "height": 600
  }
}
```

## Creating Outputs

### Creating a Literal Output

`Literal` outputs take the *exact* value provided by the `target` field, after any context expressions are reslved, and provide them as an output. 

```json
{
  "action": "OutputValue",
  "target": "This is some text that will be output exactly",
  "parameters": {
    "source": "Literal",
    "outputName": "ExampleOutput"
  }
}
```

It can then be consumed through the `Validation` context object like so:

```json
{
  "action": "SendKeys",
  "target": "${{ Definitions.TextBox }}",
  "parameters": {
    "data": "${{ Validation.ExampleOutput }}"
  }
}
```

The `"SendKeys"` example above would evaluate to be equivalent to:

```json
{
  "action": "SendKeys",
  "target": "${{ Definitions.TextBox }}",
  "parameters": {
    "data": "This is some text that will be output exactly"
  }
}
```

### Creating Output from XPath Text

`XPathText` outputs retrieve the inner text value of the element described by the `target` XPath.

Assuming that `${{ Definitions.SomeLabel }}` points to a label that has the text "This is some example text", then the following step would create the output `${{ Validation.SomeLabelText }}` with value "This is some example text".

```json
{
  "action": "OutputValue",
  "target": "${{ Definitions.SomeLabel }}",
  "parameters": {
    "source": "XPathText",
    "outputName": "SomeLabelText"
  }
}
```

### Creating output from XPath Property

Similarly, the `XPathProperty` source can be used to retrieve a property of an XPath

```json
{
  "action": "OutputValue",
  "target": "${{ Definitions.SomeLabel }}",
  "parameters": {
    "parameterName": "className",
    "source": "XPathProperty",
    "outputName": "SomeLabelClassName"
  }
}
```

## XPath Validations

### Validating an Element Exists on the Page

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.UsernameField }}",
  "state": "Exists"
}
```

### Validating an Element Does Not Exist on the Page

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotExists"
}
```

### Validating an Element is Visible on the Page

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "Visible"
}
```

### Validating an Element is Not Visisble on the Page

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.HiddenInputField }}",
  "state": "NotVisible"
}
```

### Validating the XPath Text Matches a Pattern

Checking that it contains some text

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "TextMatches",
  "parameters": {
    "pattern": "Sign In"
  }
}
```

Checking that it matches the text exactly

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "TextMatches",
  "parameters": {
    "pattern": "^Sign In$"
  }
}
```

Matching a more advanced regular expression:

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "TextMatches",
  "parameters": {
    "pattern": "^[Ss]ign[ -]?[Ii]n!?$"
  }
}
```

The above example will match "Sign in", "sign in", "signin", "sign-In", "Sign In!", etc.

Quilla uses Python syntax regular expressions for text matching. For more information on how to write regular expressions, refer to the [regular expression HOWTO](https://docs.python.org/3/howto/regex.html)

### Validating that the XPath Text Does Not Match a Pattern

The inverse of the `TextMatches` operation. The following example will be a success if and only if the text does not include the text "Sign In" anywhere.

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotTextMatches",
  "parameters": {
    "pattern": "Sign In"
  }
}
```

### Validating that the XPath Has Some Property

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "HasProperty",
  "parameters": {
    "name": "className"
  }
}
```

### Validating that the XPath Does Not Have Some Property

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotHasProperty",
  "parameters": {
    "name": "className"
  }
}
```

### Validating that the XPath Has Some Attribute

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "HasAttribute",
  "parameters": {
    "name": "class"
  }
}
```

### Validating that the XPath Does Not Have Some Attribute

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotHasAttribute",
  "parameters": {
    "name": "class"
  }
}
```

### Validating that the XPath Has Some Property With a Specific Value

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "PropertyHasValue",
  "parameters": {
    "name": "className",
    "value": "mr-3"
  }
}
```

### Validating that the XPath Does Not Have Some Property With a Specific Value

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotPropertyHasValue",
  "parameters": {
    "name": "className",
    "value": "mr-3"
  }
}
```

### Validating that the XPath Has Some Attribute With a Specific Value

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "AttributeHasValue",
  "parameters": {
    "name": "class",
    "value": "mr-3"
  }
}
```

### Validating that the XPath Does Not Have Some Attribute With a Specific Value

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.SignInButton }}",
  "state": "NotAttributeHasValue",
  "parameters": {
    "name": "class",
    "value": "mr-3"
  }
}
```

## Performing VisualParity Validation

Although it is a form of XPath validation, VisualParity require additional setup.

It is *not* required to give a specific target the same name in a Definition file/section and in the Baseline ID used for the target. However, doing so makes it easier to navigate the resulting images.

Performing VisualParity validation on a page element

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.HomePageContentContainer }}",
  "state": "VisualParity",
  "parameters": {
    "baselineID": "HomePageContentContainer"
  }
}
```

Performing VisualParity validation on a page element while ignoring some sub-elements

```json
{
  "action": "Validate",
  "type": "XPath",
  "target": "${{ Definitions.HomePageContentContainer }}",
  "state": "VisualParity",
  "parameters": {
    "baselineID": "HomePageContentContainer",
    "excludeXPaths": [
      "${{ Definitions.TodaysDateLabel }}",
      "${{ Definitions.TodaysWeatherIcon }}",
    ]
  }
}
```

## Performing URL Validations

### Validating URL Constains Some Text

```json
{
  "action": "Validate",
  "type": "URL",
  "state": "Contains",
  "target": "?q=${{ Validation.SearchQuery }}"
}
```

### Validating URL Does Not Contain Some Text

```json
{
  "action": "Validate",
  "type": "URL",
  "state": "NotContains",
  "target": "?q=${{ Validation.SearchQuery }}"
}
```

### Validating URL Matches Some Text Exactly

```json
{
  "action": "Validate",
  "type": "URL",
  "state": "Equals",
  "target": "https://www.bing.com"
}
```

### Validating URL Does Not Match Some Text Exactly

```json
{
  "action": "Validate",
  "type": "URL",
  "state": "NotEquals",
  "target": "http://www.bing.com"
}
```
