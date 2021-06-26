from enum import Enum
from typing import Type

import pytest

from quilla.common.utils import (
    DriverHolder,
    EnumResolver
)
from quilla.common.exceptions import (
    NoDriverException,
    EnumValueNotFoundException
)
from quilla.common import enums


@pytest.mark.smoke
@pytest.mark.util
class UtilTests:
    def test_driverholder_exception(self):
        '''
        Tests that any driver holder will cause an exception when trying
        to access a driver when none are set.
        '''
        holder = DriverHolder()

        assert holder._driver is None

        with pytest.raises(NoDriverException):
            holder.driver

    def test_driverholder_returns_expected(self):
        holder = DriverHolder()

        holder.driver = "Some Value"

        assert holder.driver == "Some Value"

    @pytest.mark.parametrize("enum_type", [
        enums.UITestActions,
        enums.XPathValidationStates,
        enums.URLValidationStates,
        enums.ReportType,
        enums.BrowserTargets,
        enums.OutputSources
    ])
    def test_enumresolver_can_resolve_expected(self, enum_type: Type[Enum]):
        resolver = EnumResolver()
        for val in enum_type:
            assert resolver._name_to_enum(val.value, enum_type) is val

    @pytest.mark.parametrize("enum_type", [
        enums.UITestActions,
        enums.XPathValidationStates,
        enums.URLValidationStates,
        enums.ReportType,
        enums.BrowserTargets,
        enums.OutputSources
    ])
    def test_enumresolver_raises_exception_if_no_result(self, enum_type: Type[Enum]):
        resolver = EnumResolver()

        with pytest.raises(EnumValueNotFoundException):
            resolver._name_to_enum('', enum_type)
