import pytest
import pytest_cases
from connector.oai.capability import CapabilityName, get_oauth

from connector.generated import (
    CreateAccountResponse,
    Error,
    ErrorCode,
    ErrorResponse,
)
from {name}.integration import integration
from {name}.serializers.request import (
    {pascal}CreateAccountRequest,
)

from tests.type_definitions import ClientContextManager, ResponseBodyMap


@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=["tests.test_account_provisioning.test_create_account_cases"],
)
def test_create_account(
    httpx_async_client: ClientContextManager,
    args: {pascal}CreateAccountRequest,
    response_body_map: ResponseBodyMap,
    expected_response: CreateAccountResponse | ErrorResponse,
) -> None:
    """Test ``create_account`` operation."""
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.CREATE_ACCOUNT, args.model_dump_json())

    assert response == expected_response.model_dump_json()
