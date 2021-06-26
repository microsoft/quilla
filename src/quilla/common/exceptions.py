'''
Custom exceptions for the UIValidation module
'''

from enum import Enum
from typing import Type


# Exceptions
class UIValidationException(Exception):
    '''
    Base exception for all UIValidation module exceptions
    '''


class NoDriverException(UIValidationException):
    '''
    Exception for when steps are called to action without being bound to a driver
    '''

    def __init__(self):
        super().__init__("No driver currently bound")


class FailedStepException(UIValidationException):
    '''
    Exception for when there is a failed step in the chain
    '''


class EnumValueNotFoundException(UIValidationException):
    '''
    Exception for when an enum value cannot be found by string
    value
    '''

    def __init__(self, str_value: str, enum: Type[Enum]):
        super().__init__(f'Cannot find {enum} with value {str_value}')


class InvalidContextExpressionException(UIValidationException):
    '''
    Exception caused by the context expression syntax being invalid
    '''


class InvalidOutputName(UIValidationException):
    '''
    Exception caused by an invalid output name
    '''


class InvalidBrowserStateException(UIValidationException):
    '''
    Exception caused by attempting to change the browser target
    while the browser is currently open
    '''
