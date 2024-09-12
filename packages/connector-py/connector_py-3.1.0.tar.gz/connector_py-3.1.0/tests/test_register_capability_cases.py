"""Test cases for ``Integration.info`` function."""

import typing as t

from connector.capability import CapabilityName
from connector.integration import Integration, IntegrationCapability
from connector.serializers.request import BasicCredentials, ListAccountsRequest, Request
from connector.serializers.response import ListAccountsResponse, Response

Case: t.TypeAlias = tuple[
    CapabilityName,
    dict[CapabilityName, IntegrationCapability],
]


def case_register_capability_success() -> Case:
    app_id = "test"
    integration = Integration(
        app_id=app_id,
        auth=BasicCredentials,
        exception_handlers=[],
        handle_errors=True,
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

    return capability_name, integration.capabilities
