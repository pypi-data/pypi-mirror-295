"""Tests for ``connector.integration`` module."""

import pytest
import pytest_cases
from connector.capability import CapabilityName
from connector.integration import Integration, IntegrationCapability
from connector.serializers.abstract import Info
from connector.serializers.response import Response, ResponseData


@pytest_cases.parametrize_with_cases(
    ["integration", "capability_name", "request_", "exception_type"],
    cases=[
        "tests.test_dispatch_raising_cases",
    ],
)
def test_dispatch_unhandled(
    integration: Integration,
    capability_name: CapabilityName,
    request_: str,
    exception_type: type[Exception],
) -> None:
    """Test if unhandled call to unregistered capability raises."""
    with pytest.raises(exception_type):
        integration.dispatch(capability_name, request_)


@pytest_cases.parametrize_with_cases(
    ["integration", "capability_name", "request_", "expected_response"],
    cases=[
        "tests.test_dispatch_returning_cases",
    ],
)
def test_dispatch(
    integration: Integration,
    capability_name: CapabilityName,
    request_: str,
    expected_response: Response[ResponseData],
) -> None:
    actual_response = integration.dispatch(capability_name, request_)
    assert actual_response == expected_response


@pytest_cases.parametrize_with_cases(
    ["integration", "expected_info"],
    cases=[
        "tests.test_info_cases",
    ],
)
def test_info(
    integration: Integration,
    expected_info: Info,
) -> None:
    actual_info = integration.info()
    assert actual_info == expected_info


@pytest_cases.parametrize_with_cases(
    ["capability_name", "integration_capabilities"],
    cases=[
        "tests.test_register_capability_cases",
    ],
)
def test_registration(
    capability_name: CapabilityName,
    integration_capabilities: dict[CapabilityName, IntegrationCapability],
) -> None:
    assert capability_name in integration_capabilities
