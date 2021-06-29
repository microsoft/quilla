'''
A module containing an assortment of utility classes that don't really fit in anywhere else.
These classes define shared behaviour for specific actions that some other classes require, such
as checking for the actual existence of a valid driver when attempting to retrieve the driver,
or alternatively attempting to resolve a valid enum given its type and the value associated with it.
'''


from typing import (
    Type,
    Optional,
    TypeVar
)
from enum import Enum

from selenium.webdriver.remote.webdriver import WebDriver

from quilla.common.exceptions import (
    NoDriverException,
    EnumValueNotFoundException
)


T = TypeVar('T', bound=Enum)


class DriverHolder:
    '''
    Utility class to define shared behaviour for classes that contain
    a driver property
    '''
    def __init__(self, driver: Optional[WebDriver] = None):
        self._driver = driver

    @property
    def driver(self) -> WebDriver:
        '''
        The webdriver attached to this object

        Raises:
            NoDriverException: if the internal driver is currently None
        '''
        if self._driver is None:
            raise NoDriverException
        return self._driver

    @driver.setter
    def driver(self, new_driver: Optional[WebDriver]) -> Optional[WebDriver]:
        self._driver = new_driver

        return new_driver


class EnumResolver:
    '''
    Utility class to define shared behaviour for classes that need to
    resolve string values into appropriate enums
    '''

    # ctx type omitted due to circular import
    @classmethod
    def _name_to_enum(cls, name: str, enum: Type[T], ctx=None) -> T:
        '''
        Converts a string value into the appropriate enum type.
        Useful for inner representations of the data so we're not just working with strings
        everywhere

        Args:
            ctx: the runtime context of the application
            name: the string value to resolve into an enum
            enum: the parent Enum class that contains an entry matching the name argument

        Raises:
            EnumValueNotFoundException: if this resolver fails to resolve an appropriate
                enum value
        '''
        for enum_obj in enum:
            if enum_obj.value == name:
                return enum_obj

        if ctx is not None:
            resolved_plugin_value = ctx.pm.hook.quilla_resolve_enum_from_name(name=name, enum=enum)

            if resolved_plugin_value is not None:
                return resolved_plugin_value

        raise EnumValueNotFoundException(name, enum)
