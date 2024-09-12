import pytest
import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    UnassignEntitlementResponse,
)
from {name}.integration import integration
from {name}.serializers.request import (
    {pascal}UnassignEntitlementRequest,
)

from tests.type_definitions import ClientContextManager, ResponseBodyMap

@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_updates.test_unassign_entitlement_cases",
    ],
)
def test_validate_unassign_entitlement(
    httpx_async_client: ClientContextManager,
    args: {pascal}UnassignEntitlementRequest,
    response_body_map: ResponseBodyMap,
    expected_response: UnassignEntitlementResponse | ErrorResponse,
) -> None:
    """Test ``unassign-entitlement`` operation."""
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.UNASSIGN_ENTITLEMENT, args.model_dump_json())

    assert response == expected_response.model_dump_json()
