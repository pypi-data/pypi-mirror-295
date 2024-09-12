"""Test cases for ``Integration.dispatch`` function."""

import json

from connector.capability import CapabilityName
from connector.integration import Integration
from connector.serializers.request import (
    BasicCredentials,
    ListAccountsRequest,
    Request,
)
from connector.serializers.response import (
    EncounteredErrorResponse,
    ListAccountsResponse,
    Response,
)

Case = tuple[
    Integration,
    CapabilityName,
    str,
    str,
]


def case_dispatch_not_implemented_handled() -> Case:
    integration = Integration(
        app_id="test",
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=True,
    )
    capability_name = CapabilityName.LIST_ACCOUNTS
    # don't have to care about actual request data, integration should reject the call before it touches it
    request = "{}"
    expected_response = (
        Response[EncounteredErrorResponse]
        .from_error(
            error=EncounteredErrorResponse(
                message="Capability 'list-accounts' is not implemented.",
                error_code="not_implemented",
            ),
        )
        .model_dump_json()
    )
    return integration, capability_name, request, expected_response


def case_dispatch_async_success() -> Case:
    """Calling working async method should return positive response."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=False,
    )

    capability_name = CapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    async def capability(request: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(
                accounts=[],
            ),
            raw_data=None,
        )

    request = json.dumps(
        {
            "request": {},
            "auth": {
                "model": "basic",
                "username": "test",
                "password": "test",
            },
        }
    )

    expected_response = Response(
        response=ListAccountsResponse(
            accounts=[],
        ),
        raw_data=None,
        page=None,
        error=None,
    ).model_dump_json()

    return integration, capability_name, request, expected_response


def case_dispatch_sync_success() -> Case:
    """Calling working sync method should return positive response."""
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=False,
    )

    capability_name = CapabilityName.LIST_ACCOUNTS

    @integration.register_capability(capability_name)
    def capability(request: Request[ListAccountsRequest]) -> Response[ListAccountsResponse]:
        return Response[ListAccountsResponse](
            response=ListAccountsResponse(
                accounts=[],
            ),
            raw_data=None,
        )

    request = json.dumps(
        {
            "request": {},
            "auth": {
                "model": "basic",
                "username": "test",
                "password": "test",
            },
        }
    )

    expected_response = Response(
        response=ListAccountsResponse(
            accounts=[],
        ),
        raw_data=None,
        page=None,
        error=None,
    ).model_dump_json()

    return integration, capability_name, request, expected_response
