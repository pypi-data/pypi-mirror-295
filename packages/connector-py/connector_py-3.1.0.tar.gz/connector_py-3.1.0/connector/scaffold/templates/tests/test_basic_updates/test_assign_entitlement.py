import pytest
import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth
from {name}.serializers.request import (
    {pascal}AssignEntitlementRequest,
)
from connector.generated import (
    AssignEntitlementResponse,
)
from {name}.integration import integration

from tests.type_definitions import ClientContextManager, ResponseBodyMap

@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_updates.test_assign_entitlement_cases",
    ],
)
def test_assign_entitlement(
    httpx_async_client: ClientContextManager,
    args: {pascal}AssignEntitlementRequest,
    response_body_map: ResponseBodyMap,
    expected_response: AssignEntitlementResponse,
) -> None:
    """Test ``assign-entitlement`` operation."""
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.ASSIGN_ENTITLEMENT, args.model_dump_json())

    assert response == expected_response.model_dump_json()
