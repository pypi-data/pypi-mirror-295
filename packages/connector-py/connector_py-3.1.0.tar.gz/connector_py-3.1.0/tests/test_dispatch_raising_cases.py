"""Test cases for ``Integration.dispatch`` function.

Those cases should lead to raised error.
"""

import json

from connector.capability import CapabilityName
from connector.integration import Integration
from connector.serializers.request import (
    BasicCredentials,
    ListAccountsRequest,
    Request,
)
from connector.serializers.response import (
    ListAccountsResponse,
    Response,
)

Case = tuple[
    Integration,
    CapabilityName,
    str,
    type[Exception],
]


def case_dispatch_not_implemented_handled() -> Case:
    """Unhandled call to unimplemented capability should raise."""
    integration = Integration(
        app_id="test",
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=False,
    )
    capability_name = CapabilityName.LIST_ACCOUNTS
    # don't have to care about actual request data, integration should reject the call before it touches it
    request = "{}"
    exception_type = NotImplementedError
    return integration, capability_name, request, exception_type


def case_dispatch_async_not_handled_error() -> Case:
    """Unhandled error in async capability should raise."""
    integration = Integration(
        app_id="test",
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=False,
    )

    class CustomException(Exception):
        pass

    @integration.register_capability(CapabilityName.LIST_ACCOUNTS)
    async def list_accounts(req: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        raise CustomException

    capability_name = CapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"model": "basic", "username": "user", "password": "pass"},
            "request": {},
        }
    )
    exception_type = CustomException

    return integration, capability_name, request, exception_type


def case_dispatch_sync_not_handled_error() -> Case:
    """Unhandled error in sync capability should raise."""
    integration = Integration(
        app_id="test",
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=False,
    )

    class CustomException(Exception):
        pass

    @integration.register_capability(CapabilityName.LIST_ACCOUNTS)
    def list_accounts(req: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        raise CustomException

    capability_name = CapabilityName.LIST_ACCOUNTS
    request = json.dumps(
        {
            "auth": {"model": "basic", "username": "user", "password": "pass"},
            "request": {},
        }
    )
    exception_type = CustomException

    return integration, capability_name, request, exception_type
