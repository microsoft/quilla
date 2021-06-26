'''
Module with all requried enums for the UIValidation
'''

from enum import Enum


# Enums
class ValidationTypes(Enum):
    '''
    The currently-supported types of validation allowed
    '''
    XPATH = 'XPath'
    URL = 'URL'


class ValidationStates(Enum):
    '''
    Base class for validation state enums
    '''


class XPathValidationStates(ValidationStates):
    '''
    States that the XPath validation class recognizes
    '''
    EXISTS = 'Exists'
    NOT_EXISTS = 'NotExists'
    VISIBLE = 'Visible'
    NOT_VISIBLE = 'NotVisible'
    TEXT_MATCHES = 'TextMatches'
    NOT_TEXT_MATCHES = 'NotTextMatches'
    HAS_PROPERTY = 'HasProperty'
    NOT_HAS_PROPERTY = 'NotHasProperty'
    PROPERTY_HAS_VALUE = 'PropertyHasValue'
    NOT_PROPERTY_HAS_VALUE = 'NotPropertyHasValue'
    HAS_ATTRIBUTE = 'HasAttribute'
    NOT_HAS_ATTRIBUTE = 'NotHasAttribute'
    ATTRIBUTE_HAS_VALUE = 'AttributeHasValue'
    NOT_ATTRIBUTE_HAS_VALUE = 'NotAttributeHasValue'


class URLValidationStates(ValidationStates):
    '''
    States that the URL validation class recognizes
    '''
    CONTAINS = 'Contains'
    NOT_CONTAINS = 'NotContains'
    EQUALS = 'Equals'
    NOT_EQUALS = 'NotEquals'
    MATCHES = 'Matches'
    NOT_MATCHES = 'NotMatches'


class UITestActions(Enum):
    '''
    All supported UI test actions
    '''
    CLICK = 'Click'
    CLEAR = 'Clear'
    SEND_KEYS = 'SendKeys'
    WAIT_FOR_EXISTENCE = 'WaitForExistence'
    WAIT_FOR_VISIBILITY = 'WaitForVisibility'
    NAVIGATE_TO = 'NavigateTo'
    VALIDATE = 'Validate'
    REFRESH = "Refresh"
    ADD_COOKIES = "AddCookies"
    SET_COOKIES = "SetCookies"
    REMOVE_COOKIE = "RemoveCookie"
    CLEAR_COOKIES = "ClearCookies"
    NAVIGATE_FORWARD = "NavigateForward"
    NAVIGATE_BACK = "NavigateBack"
    SET_BROWSER_SIZE = "SetBrowserSize"
    HOVER = "Hover"
    OUTPUT_VALUE = "OutputValue"


class ReportType(Enum):
    '''
    All the currently supported report types
    '''
    VALIDATION = "Validation"
    STEP_FAILURE = "StepFailure"


class BrowserTargets(Enum):
    '''
    All the currently supported browser targets
    '''
    FIREFOX = "Firefox"
    CHROME = "Chrome"
    EDGE = "Edge"


class OutputSources(Enum):
    '''
    Supported sources for the OutputValue action
    '''
    LITERAL = 'Literal'
    XPATH_TEXT = 'XPathText'
    XPATH_PROPERTY = 'XPathProperty'
